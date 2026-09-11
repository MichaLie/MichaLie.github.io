#!/usr/bin/env python3
"""Synchronize portal summaries from local child catalogs; never publish."""
import argparse
from datetime import date
import hashlib
import json
import re
from xml.sax.saxutils import escape

import validate_portal as portal


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def check_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("date must use YYYY-MM-DD")
    date.fromisoformat(value)


def sync(version: str, modified: str) -> dict:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("version must use MAJOR.MINOR.PATCH")
    check_date(modified)
    root = portal.ROOT
    catalog = json.loads((root / "catalog.json").read_text())
    metadata = json.loads((root / "metadata.jsonld").read_text())
    html = (root / "index.html").read_text()
    ids = [entry["id"] for entry in catalog["catalogs"]]
    if len(ids) != 3 or set(ids) != set(portal.CHILDREN):
        raise ValueError("portal must contain exactly the three canonical child catalogs")
    locked = []
    for entry in catalog["catalogs"]:
        relative_path, public_url = portal.CHILDREN[entry["id"]]
        path = portal.local_child_path(relative_path)
        payload = path.read_bytes()
        rows = json.loads(payload)
        child = json.loads(path.with_name("resource_metadata.json").read_text())
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"expected a nonempty catalog array: {path}")
        if child["identifier"] != entry["id"] or child["data_file"] != path.name:
            raise ValueError(f"child identity/data file mismatch: {path}")
        check_date(child["modified"])
        entry.update(record_count=len(rows), version=child["resource_version"])
        locked.append({
            "id": entry["id"], "version": child["resource_version"],
            "updated": child["modified"], "record_count": len(rows),
            "data_distribution": public_url,
            "sha256": hashlib.sha256(payload).hexdigest(),
        })

    catalog.update(version=version, date_modified=modified, release_ref=None)
    schema = json.loads((root / "catalog.schema.json").read_text())
    portal.Draft202012Validator(schema, format_checker=portal.FormatChecker()).validate(catalog)
    metadata["schema:version"] = version
    metadata["dct:modified"]["@value"] = modified
    metadata["schema:numberOfItems"] = 3
    metadata["prov:wasGeneratedBy"] = {
        "@type": "prov:Activity", "dct:type": "Local preview build; release not yet authorized",
    }
    by_id = {entry["id"]: entry for entry in catalog["catalogs"]}
    dataset_ids = [dataset["@id"] for dataset in metadata["dcat:dataset"]]
    if len(dataset_ids) != 3 or set(dataset_ids) != set(by_id):
        raise ValueError("metadata must contain exactly the three canonical child datasets")
    for dataset in metadata["dcat:dataset"]:
        entry = by_id[dataset["@id"]]
        dataset["schema:numberOfItems"] = entry["record_count"]
        dataset["schema:version"] = entry["version"]

    locked_by_id = {entry["id"]: entry for entry in locked}
    card_ids = [match[2] for match in portal.CARD_PATTERN.finditer(html)]
    if len(card_ids) != 3 or set(card_ids) != set(by_id):
        raise ValueError("expected exactly one card per canonical child ID")

    def update_card(match):
        entry = locked_by_id[match[2]]
        content, counts = re.subn(
            r'(<span class="count c-(?:bio|agent|code)">)\d+(</span>)',
            lambda value: f"{value[1]}{entry['record_count']}{value[2]}", match[3],
        )
        label = f"v{entry['version']} · updated {portal.format_lock_date(entry['updated'])}"
        content, dates = re.subn(r'(<span class="vdate">)[^<]+(</span>)',
            lambda value: value[1] + label + value[2], content)
        if (counts, dates) != (1, 1):
            raise ValueError(f"expected one count/date in card {entry['id']}")
        return match[1] + content + match[4]

    html = portal.CARD_PATTERN.sub(update_card, html)
    html, metadata_matches = re.subn(
        r'(<script id="fair-catalog-metadata" type="application/ld\+json">).*?(</script>)',
        lambda match: match[1] + "\n" + json_text(metadata) + "  " + match[2],
        html, flags=re.DOTALL,
    )
    if metadata_matches != 1:
        raise ValueError("expected one embedded metadata block")

    sitemap_rows = [("https://michalie.github.io/", modified)]
    sitemap_rows.extend((entry["id"], entry["updated"]) for entry in locked)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{escape(url)}</loc><lastmod>{updated}</lastmod></url>\n" for url, updated in sitemap_rows)
    sitemap += "</urlset>\n"
    # All inputs and substitutions are checked before the first file is written.
    outputs = {
        "catalog.json": json_text(catalog),
        "child_catalogs.lock.json": json_text({"lock_version": 1, "generated": modified, "catalogs": locked}),
        "metadata.jsonld": json_text(metadata), "index.html": html, "sitemap.xml": sitemap,
    }
    for name, content in outputs.items():
        (root / name).write_text(content, encoding="utf-8")
    return {"version": version, "date": modified, "counts": [entry["record_count"] for entry in locked]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="candidate portal version")
    parser.add_argument("--date", required=True, help="candidate modification date (YYYY-MM-DD)")
    args = parser.parse_args()
    print(json.dumps(sync(args.version, args.date)))
