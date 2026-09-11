"""Exercise local, standalone and public catalog synchronization in isolation."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import ValidationError

import validate_portal as portal
from sync_catalogs import sync


class PortalSynchronizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "Portal"
        shutil.copytree(
            portal.ROOT, self.root,
            ignore=shutil.ignore_patterns(".git", "repos", "tests", "evidence", "__pycache__"),
        )
        self.lock_path = self.root / "child_catalogs.lock.json"
        self.lock = json.loads(self.lock_path.read_text())
        self.addCleanup(patch.stopall)
        patch.object(portal, "ROOT", self.root).start()
        patch.object(portal, "LOCK_PATH", self.lock_path).start()

    def save_lock(self):
        self.lock_path.write_text(json.dumps(self.lock))

    def install_children(self, *, nested=False):
        parent = self.root / "repos" if nested else self.root.parent
        paths = []
        for entry in self.lock["catalogs"]:
            relative_path, _ = portal.CHILDREN[entry["id"]]
            path = parent / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = json.dumps([{}] * entry["record_count"]).encode()
            path.write_bytes(payload)
            path.with_name("resource_metadata.json").write_text(json.dumps({
                "identifier": entry["id"], "resource_version": entry["version"],
                "modified": entry["updated"], "data_file": path.name,
            }))
            entry["sha256"] = hashlib.sha256(payload).hexdigest()
            paths.append(path)
        self.save_lock()
        return paths

    def validate(self, **kwargs):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = portal.main(**kwargs)
        return code, output.getvalue()

    def test_standalone_uses_lock_without_network(self):
        with patch.object(portal, "urlopen", side_effect=AssertionError("unexpected network")):
            code, output = self.validate()
        self.assertEqual(code, 0, output)
        self.assertIn("SOURCE: lock:", output)

    def test_sibling_checkout_is_checked_and_preferred(self):
        self.install_children()
        relative_path = next(iter(portal.CHILDREN.values()))[0]
        decoy = self.root / "repos" / relative_path
        decoy.parent.mkdir(parents=True)
        decoy.write_text("[]")
        code, output = self.validate()
        self.assertEqual(code, 0, output)
        self.assertIn("SOURCE: local:../Foundation_models/", output)

    def test_historical_nested_checkout_remains_supported(self):
        self.install_children(nested=True)
        code, output = self.validate()
        self.assertEqual(code, 0, output)
        self.assertIn("SOURCE: local:repos/Foundation_models/", output)

    def test_same_count_content_change_fails_checksum(self):
        path = self.install_children()[0]
        records = json.loads(path.read_text())
        records[0]["changed"] = True
        path.write_text(json.dumps(records))
        code, output = self.validate()
        self.assertEqual(code, 1, output)
        self.assertIn("child SHA-256 differs from lock", output)

    def test_child_version_and_date_must_match_lock(self):
        path = self.install_children()[0].with_name("resource_metadata.json")
        metadata = json.loads(path.read_text())
        metadata.update(resource_version="99.0.0", modified="2000-01-01")
        path.write_text(json.dumps(metadata))
        code, output = self.validate()
        self.assertEqual(code, 1, output)
        self.assertIn("local child version differs from lock", output)
        self.assertIn("local child modified date differs from lock", output)

    def test_remote_forces_public_bytes_even_when_siblings_exist(self):
        self.install_children()
        with patch.object(portal, "urlopen", side_effect=lambda *a, **k: io.BytesIO(b"[]")) as request:
            code, output = self.validate(remote=True)
        self.assertEqual(code, 1, output)
        self.assertEqual(request.call_count, 3)
        self.assertIn("SOURCE: remote:https://", output)
        self.assertNotIn("SOURCE: local:", output)

    def test_invalid_calendar_date_fails_cleanly(self):
        self.lock["catalogs"][0]["updated"] = "2026-02-30"
        self.save_lock()
        code, output = self.validate()
        self.assertEqual(code, 1, output)
        self.assertIn("lacks a valid updated date", output)

    def test_sync_updates_all_summaries_and_is_repeatable(self):
        path = self.install_children()[0]
        records = json.loads(path.read_text())
        records.append({"synthetic_private_record_marker": True})
        path.write_text(json.dumps(records))
        metadata_path = path.with_name("resource_metadata.json")
        child = json.loads(metadata_path.read_text())
        child.update(resource_version="99.0.0", modified="2026-09-11")
        metadata_path.write_text(json.dumps(child))
        sync("99.1.0", "2026-09-11")
        code, output = self.validate()
        self.assertEqual(code, 0, output)
        names = ["catalog.json", "metadata.jsonld", "child_catalogs.lock.json", "index.html", "sitemap.xml"]
        first = {name: (self.root / name).read_bytes() for name in names}
        sync("99.1.0", "2026-09-11")
        self.assertEqual(first, {name: (self.root / name).read_bytes() for name in names})
        catalog = json.loads(first["catalog.json"])
        self.assertEqual(catalog["catalogs"][0]["record_count"], len(records))
        self.assertIsNone(catalog["release_ref"])
        self.assertIn(b"2026-09-11", first["sitemap.xml"])
        self.assertNotIn(b"synthetic_private_record_marker", b"".join(first.values()))

    def test_sync_preserves_card_identity_when_catalog_order_changes(self):
        self.install_children()
        path = self.root / "catalog.json"
        catalog = json.loads(path.read_text())
        catalog["catalogs"].reverse()
        path.write_text(json.dumps(catalog))
        sync("99.1.0", "2026-09-11")
        code, output = self.validate()
        self.assertEqual(code, 0, output)
        by_id = {entry["id"]: entry for entry in catalog["catalogs"]}
        for card in portal.CARD_PATTERN.finditer((self.root / "index.html").read_text()):
            self.assertIn(f'>{by_id[card[2]]["record_count"]}</span>', card[3])

    def test_validator_rejects_counts_assigned_to_wrong_cards(self):
        self.install_children()
        path = self.root / "index.html"
        html = path.read_text()
        counts = [self.lock["catalogs"][i]["record_count"] for i in (0, 2)]
        html = html.replace(f'c-bio">{counts[0]}<', f'c-bio">{counts[1]}<')
        html = html.replace(f'c-code">{counts[1]}<', f'c-code">{counts[0]}<')
        path.write_text(html)
        catalog_path = self.root / "catalog.json"
        catalog = json.loads(catalog_path.read_text())
        catalog["catalogs"].reverse()
        catalog_path.write_text(json.dumps(catalog))
        code, output = self.validate()
        self.assertEqual(code, 1, output)
        self.assertIn("router card count differs", output)

    def test_malformed_child_inputs_leave_all_outputs_unchanged(self):
        path = self.install_children()[0].with_name("resource_metadata.json")
        metadata = json.loads(path.read_text())
        names = ["catalog.json", "child_catalogs.lock.json", "metadata.jsonld", "index.html", "sitemap.xml"]
        before = {name: (self.root / name).read_bytes() for name in names}
        for updates in ({"resource_version":"not-a-version"}, {"modified":"20260911"}, {"modified":"2026-02-30"}):
            with self.subTest(updates=updates):
                path.write_text(json.dumps({**metadata, **updates}))
                with self.assertRaises((ValueError, ValidationError)):
                    sync("99.1.0", "2026-09-11")
                self.assertEqual(before, {name: (self.root / name).read_bytes() for name in names})


if __name__ == "__main__":
    unittest.main()
