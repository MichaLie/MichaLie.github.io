# Changelog

All notable public changes to this collection are documented here.

## 2.2.1 — 2026-08-14

- Added a visible version-and-date line to each catalog card so the most
  recent published update of every index is legible at a glance. The lines
  are pinned to `child_catalogs.lock.json` (new per-catalog `updated` field)
  by a new validator check, so they refresh automatically with every future
  child release.
- Synchronized with the presentation-only v2.1.1 releases of all three child
  catalogs, which added the same version-and-date badge to their headers.
  Record counts, evidence, and distribution SHA-256 checksums are unchanged.
- Brought the `dct:modified` date in the DCAT metadata in step with
  `catalog.json` (it had lagged at 2026-08-11 through the v2.2.0 release).

## 2.2.0 — 2026-08-13

- Synchronized the portal with the v2.1.0 releases of all three child
  catalogs after their 2026-08-13 content refresh: Biological Foundation
  Models 345 → 390 records, Autonomous Science Agents 372 → 438 records,
  AI Coding & Data Agents 43 → 60 records. Updated `catalog.json`,
  `child_catalogs.lock.json` (new distribution SHA-256 checksums),
  `metadata.jsonld`, and the visible index cards accordingly.
- No portal-level scope, licence, or governance changes.

## 2.1.0 — 2026-08-11

- Added bio.tools, the ELIXIR tools registry, as a related ecosystem resource
  in the visible ecosystem section, `related_resources`, and the DCAT and
  Schema.org relation metadata. The registry is the primary discovery point
  for established bioinformatics software; the three indexes here focus on
  the recent AI-native generation of models, agents, and assistants, which a
  coverage check on 2026-08-11 found largely absent from the registry.
- Catalog records, counts, evidence, and child-catalog distribution
  checksums are unchanged.

## 2.0.1 — 2026-07-14

- Increased primary descriptive, navigation, community-resource, FAIR-note, and contact text for more comfortable reading across the portal.
- Synchronized the portal and child-catalog version references to the presentation-only v2.0.1 release; catalog records, counts, evidence, and distribution checksums are unchanged.

## 2.0.0 — 2026-07-14

- Reorganized the entry page around researcher needs and three specialist indexes.
- Added FAIR-oriented collection metadata, schema, provenance, licences, versioning, and machine-readable discovery.
- Added ELIXIR-CZ community-resource links for Alphafoldology and ELIXIR-CZ services.
- Added a reproducible portal maintenance and release protocol with deterministic validation.
- Refined the visual system across the collection for clearer navigation, responsive use, and accessibility.

No DOI is assigned to this release.
