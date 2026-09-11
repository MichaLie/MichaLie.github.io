# Changelog

All notable public changes to this collection are documented here.

## 2.3.0 — 2026-09-11

- Synchronized the three v2.2.0 catalogs: Biological Foundation Models
  390 → 400, Autonomous Science Agents 438 → 458, and Coding & Data Agents
  60 → 61. Counts, versions, modification dates, distribution checksums,
  visible cards, JSON-LD and sitemap agree with the canonical child files.
- Added `sync_catalogs.py` for repeatable local synchronization. Validation
  now checks sibling checkouts as well as the historical nested layout,
  including child resource identity, version and date. Card updates and
  validation use catalog identity rather than array order, and malformed
  child metadata is rejected before portal files are written. Eleven
  regression tests cover these behaviors and run in the quality workflow.
- Rechecked related resources and removed bio.tools' volatile record count.
  Its canonical link is retained while the upstream site returns HTTP 521;
  that failed check does not advance its evidence-verification date.
- Recorded the baseline, source adjudications, independent cross-reviews,
  local browser checks and publication sequence in `evidence/`. Set the
  immutable release reference after owner review and publication authorization.

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
