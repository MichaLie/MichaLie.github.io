#!/usr/bin/env python3
"""Validate the local router against its machine-readable and child catalogs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent
CARD_PATTERN = re.compile(r'(<a class="card" href="([^"]+)">)(.*?)(</a>)', re.DOTALL)
CHILDREN = {
    "https://michalie.github.io/bio-foundation-models-wiki/": (
        Path("Foundation_models/models_final.json"),
        "https://michalie.github.io/bio-foundation-models-wiki/models_final.json",
    ),
    "https://michalie.github.io/autonomous-stem-agents-wiki/": (
        Path("Autonomous_Agents/agents_final.json"),
        "https://michalie.github.io/autonomous-stem-agents-wiki/agents_final.json",
    ),
    "https://michalie.github.io/research-coding-agents-wiki/": (
        Path("Coding_Agents/tools.json"),
        "https://michalie.github.io/research-coding-agents-wiki/tools.json",
    ),
}
EXPECTED_RELATED_RESOURCES = {
    "https://karelberka.github.io/Alphafoldology/",
    "https://www.elixir-czech.cz/services",
    "https://bio.tools/",
}
LOCK_PATH = ROOT / "child_catalogs.lock.json"


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capture = False
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "script" and values.get("id") == "fair-catalog-metadata" and values.get("type") == "application/ld+json":
            self.capture = True

    def handle_data(self, data):
        if self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.capture:
            self.capture = False


def format_lock_date(iso_date: str) -> str:
    """Render a lock-file ISO date the way the visible cards print it (e.g. 14 Aug 2026)."""
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    value = date.fromisoformat(iso_date)
    return f"{value.day} {months[value.month - 1]} {value.year}"


def local_child_path(relative_path: Path) -> Path:
    """Find a sibling checkout, retaining the historical nested layout."""
    sibling = ROOT.parent / relative_path
    if sibling.is_file():
        return sibling
    return ROOT / "repos" / relative_path


def load_json_bytes(payload: bytes, source: str) -> tuple[list, str, str]:
    data = json.loads(payload.decode("utf-8"))
    return data, source, hashlib.sha256(payload).hexdigest()


def load_child_catalog(local_path: Path, public_url: str, force_remote: bool) -> tuple[list, str, str]:
    if local_path.is_file() and not force_remote:
        return load_json_bytes(local_path.read_bytes(), f"local:{os.path.relpath(local_path, ROOT)}")
    request = Request(public_url, headers={"User-Agent": "AI-for-Science-portal-validator/2.0"})
    with urlopen(request, timeout=30) as response:
        payload = response.read(50_000_001)
    if len(payload) > 50_000_000:
        raise ValueError(f"child catalog exceeds 50 MB: {public_url}")
    return load_json_bytes(payload, f"remote:{public_url}")


def main(release: bool = False, remote: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    locked_catalogs = {entry["id"]: entry for entry in lock.get("catalogs", [])}
    schema = json.loads((ROOT / "catalog.schema.json").read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(catalog):
        errors.append(f"catalog.json {'/'.join(map(str, error.absolute_path))}: {error.message}")
    catalog_ids = [entry.get("id") for entry in catalog.get("catalogs", [])]
    if len(catalog_ids) != 3 or set(catalog_ids) != set(CHILDREN):
        errors.append("catalog.json must contain each canonical child ID exactly once")

    expected_counts = {}
    child_sources = []
    for entry in catalog.get("catalogs", []):
        child_config = CHILDREN.get(entry.get("id"))
        if child_config is None:
            errors.append(f"unknown child catalog ID: {entry.get('id')}")
            continue
        locked = locked_catalogs.get(entry["id"])
        if locked is None:
            errors.append(f"child catalog is missing from child_catalogs.lock.json: {entry['id']}")
            continue
        relative_path, public_url = child_config
        local_path = local_child_path(relative_path)
        if public_url != entry.get("data_distribution") or public_url != locked.get("data_distribution"):
            errors.append(f"child distribution mismatch: {entry['id']}")
        if entry.get("version") != locked.get("version"):
            errors.append(f"child version differs from lock: {entry['id']}")
        if local_path.is_file() or remote:
            try:
                child, source, digest = load_child_catalog(local_path, public_url, force_remote=remote)
            except Exception as exc:
                errors.append(f"cannot load child catalog {entry.get('id')}: {exc}")
                continue
            if not isinstance(child, list):
                errors.append(f"child catalog is not a JSON array: {entry.get('id')}")
                continue
            actual = len(child)
            child_sources.append(source)
            if digest != locked.get("sha256"):
                errors.append(f"child SHA-256 differs from lock: {entry['id']} ({digest})")
            if not remote:
                metadata_path = local_path.with_name("resource_metadata.json")
                try:
                    child_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                except (OSError, ValueError) as exc:
                    errors.append(f"cannot read local child metadata for {entry['id']}: {exc}")
                else:
                    if child_metadata.get("identifier") != entry["id"]:
                        errors.append(f"local child identifier differs from portal: {entry['id']}")
                    if child_metadata.get("resource_version") != locked.get("version"):
                        errors.append(f"local child version differs from lock: {entry['id']}")
                    if child_metadata.get("modified") != locked.get("updated"):
                        errors.append(f"local child modified date differs from lock: {entry['id']}")
        else:
            actual = locked.get("record_count")
            child_sources.append(f"lock:{LOCK_PATH.name}#{entry['id']}")
        if actual != locked.get("record_count"):
            errors.append(f"child count differs from lock: {entry['id']} ({actual})")
        expected_counts[entry["id"]] = actual
        if entry.get("record_count") != actual:
            errors.append(f"{entry['id']}: catalog.json says {entry.get('record_count')}, canonical child has {actual}")

    standalone = json.loads((ROOT / "metadata.jsonld").read_text(encoding="utf-8"))
    parser = MetadataParser()
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    parser.feed(html)
    if not parser.parts:
        errors.append("index.html: embedded FAIR catalog metadata missing")
        embedded = {}
    else:
        embedded = json.loads("".join(parser.parts))
        if embedded != standalone:
            errors.append("index.html embedded JSON-LD differs from metadata.jsonld")

    datasets = {entry["@id"]: entry for entry in standalone.get("dcat:dataset", [])}
    for identifier, count in expected_counts.items():
        if datasets.get(identifier, {}).get("schema:numberOfItems") != count:
            errors.append(f"metadata.jsonld count mismatch for {identifier}")
        if datasets.get(identifier, {}).get("schema:version") != locked_catalogs.get(identifier, {}).get("version"):
            errors.append(f"metadata.jsonld child version mismatch for {identifier}")

    if set(locked_catalogs) != set(CHILDREN):
        errors.append("child_catalogs.lock.json IDs differ from the supported child catalogs")

    related = catalog.get("related_resources", [])
    related_ids = [entry.get("id") for entry in related]
    if len(related_ids) != len(set(related_ids)):
        errors.append("catalog.json related_resources contains duplicate IDs")
    if set(related_ids) != EXPECTED_RELATED_RESOURCES:
        errors.append(f"catalog.json related resource IDs differ from expected set: {related_ids}")
    for entry in related:
        if entry.get("included_in_child_catalog") is not False:
            errors.append(f"related resource must remain outside child catalogs: {entry.get('id')}")

    relation_value = standalone.get("dct:relation", [])
    if isinstance(relation_value, dict):
        relation_value = [relation_value]
    relation_ids = {entry.get("@id") for entry in relation_value if isinstance(entry, dict)}
    if relation_ids != EXPECTED_RELATED_RESOURCES:
        errors.append(f"metadata.jsonld dct:relation differs from catalog related resources: {sorted(relation_ids)}")
    mention_ids = {entry.get("@id") for entry in standalone.get("schema:mentions", []) if isinstance(entry, dict)}
    if not EXPECTED_RELATED_RESOURCES.issubset(mention_ids):
        errors.append("metadata.jsonld schema:mentions omits a related resource")
    related_links = set(standalone.get("schema:relatedLink", []))
    if not EXPECTED_RELATED_RESOURCES.issubset(related_links):
        errors.append("metadata.jsonld schema:relatedLink omits a related landing page")
    for identifier in EXPECTED_RELATED_RESOURCES:
        if f'href="{identifier}"' not in html:
            errors.append(f"index.html omits visible related-resource link: {identifier}")
    if 'id="ecosystem-title"' not in html:
        errors.append("index.html omits the related community/infrastructure section")

    cards = list(CARD_PATTERN.finditer(html))
    card_ids = [card[2] for card in cards]
    if len(card_ids) != 3 or set(card_ids) != set(CHILDREN):
        errors.append("router must contain exactly one card for each canonical child ID")
    cards_by_id = {card[2]: card[3] for card in cards}
    canonical_counts = [entry["record_count"] for entry in catalog.get("catalogs", [])]
    for entry in catalog.get("catalogs", []):
        card = cards_by_id.get(entry["id"], "")
        counts = re.findall(r'<span class="count c-(?:bio|agent|code)">(\d+)</span>', card)
        if counts != [str(entry["record_count"])]:
            errors.append(f"router card count differs from catalog count for {entry['id']}")
        locked = locked_catalogs.get(entry["id"])
        if locked is None:
            continue
        try:
            updated = locked.get("updated") or ""
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated):
                raise ValueError("expected YYYY-MM-DD")
            formatted_date = format_lock_date(updated)
        except (ValueError, TypeError):
            errors.append(f"child_catalogs.lock.json entry lacks a valid updated date: {entry['id']}")
            continue
        card_dates = re.findall(r'<span class="vdate">([^<]+)</span>', card)
        if card_dates != [f"v{locked['version']} · updated {formatted_date}"]:
            errors.append(f"router card version/date differs from lock for {entry['id']}")

    if re.search(r'href=["\']repos/', html):
        errors.append("index.html contains preview-only child routes")
    for entry in catalog.get("catalogs", []):
        landing_page = entry.get("landing_page")
        if not landing_page or html.count(f'href="{landing_page}"') < 2:
            errors.append(f"index.html must route both card and need link to canonical child: {landing_page}")

    for href in ("catalog.json", "metadata.jsonld", "catalog.schema.json", "child_catalogs.lock.json", "LICENSE-CONTENT.md", "LICENSE-CODE", "assets/elixir-cz-logo.svg", "assets/img-logo-color-transparent.png"):
        if not (ROOT / href).is_file():
            errors.append(f"missing portal artifact: {href}")

    if "preview" in catalog.get("version", "").casefold() or "-rc" in catalog.get("version", "").casefold():
        message = "portal version remains a preview/release candidate"
        (errors if release else warnings).append(message)
    if catalog.get("license") != "https://creativecommons.org/licenses/by/4.0/":
        errors.append("portal content licence must resolve to CC BY 4.0")
    if catalog.get("code_license") != "https://spdx.org/licenses/MIT.html":
        errors.append("portal code licence must resolve to MIT")
    publisher = catalog.get("publisher") or {}
    if publisher.get("type") != "Person" or publisher.get("name") != "Michaela Liegertová":
        errors.append("portal publisher must be the named individual, not an affiliation or dedication")
    if catalog.get("release_ref") is None:
        message = "portal release_ref remains null until an explicitly authorized immutable release exists"
        (errors if release else warnings).append(message)
    elif release:
        expected_release_ref = catalog["repository"].rstrip("/") + "/releases/tag/v" + catalog["version"]
        if catalog["release_ref"].rstrip("/") != expected_release_ref:
            errors.append(f"portal release_ref must match repository and version (expected {expected_release_ref})")
    if standalone.get("dct:license", {}).get("@id") != catalog.get("license"):
        errors.append("metadata.jsonld licence differs from catalog.json")
    if standalone.get("schema:version") != catalog.get("version"):
        errors.append("metadata.jsonld version differs from catalog.json")
    if standalone.get("dct:modified", {}).get("@value") != catalog.get("date_modified"):
        errors.append("metadata.jsonld modified date differs from catalog.json")
    if standalone.get("schema:numberOfItems") != 3:
        errors.append("metadata.jsonld must describe exactly three child catalogs")
    provenance_ref = standalone.get("prov:wasGeneratedBy", {}).get("@id")
    if provenance_ref != catalog.get("release_ref"):
        errors.append("metadata.jsonld release reference differs from catalog.json")
    if standalone.get("dct:publisher", {}).get("schema:name") != publisher.get("name"):
        errors.append("metadata.jsonld publisher differs from catalog.json")

    print(f"PORTAL VALIDATION catalogs={len(canonical_counts)} counts={canonical_counts}")
    for source in child_sources:
        print(f"SOURCE: {source}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--remote", action="store_true", help="force comparison with public child distributions")
    args = parser.parse_args()
    raise SystemExit(main(release=args.release, remote=args.remote))
