# Portal local refresh — 2026-11-06

Local **2.5.0** candidate on branch `agent/v2.5.0-catalog-sync`, synchronized with the three local **2.4.0** catalog previews. `release_ref` remains null. Nothing was pushed or published.

## Synchronized catalogs

| Catalog | October (2.3.0) | November (2.4.0) |
|---|---|---|
| Biological Foundation Models | 486 | 538 |
| Autonomous Science Agents | 542 | 610 |
| AI Coding & Data Agents | 71 | 78 |

`python3 sync_catalogs.py --version 2.5.0 --date 2026-11-06` derived counts, versions, dates and SHA-256 checksums from the local child catalogs. It updated `catalog.json`, `child_catalogs.lock.json`, the standalone and embedded JSON-LD, the visible cards and the sitemap. The child catalogs' own audit notes record their evidence: `evidence/DISCOVERY_AUDIT_2026-11-06.md` (Foundation Models, Autonomous Agents) and `evidence/LIVE_AUDIT_2026-11-06.md` (Coding Agents).

## Checks

- `python3 -m unittest discover -s tests`: 11 tests pass.
- `python3 validate_portal.py`: pass against the sibling child catalogs; one expected warning for the null release reference.
- `validate_portal.py --remote` is expected to fail until the three child releases are published, because the live distributions are still the October files. Publish the children first, then re-run it.
- External links on the page (12): all HTTP 200. See `portal-link-audit-2026-11-06.json`.
- Browser review on a local HTTP server: portal at 1440 and 390 px; the three catalogs at 1440, 1024, 900 and 390 px. No document overflow and no console errors; version badges read v2.4.0 · updated 2026-11-06. At 900 px and below, controls and table headers are static. Above 900 px the table header is sticky under the controls; at 1440 px it is aligned exactly, at 1024 px the Foundation Models header sits about 10 px below the controls. The live 2.3.0 page shows the same 10 px offset at 1024 px, so this predates this release and is left for a separate layout fix. The Coding Agents data-class selection was exercised and behaves as on the live site.
