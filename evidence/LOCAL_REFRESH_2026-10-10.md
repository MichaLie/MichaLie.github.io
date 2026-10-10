# Portal local refresh — 2026-10-10

Local **2.4.0** candidate on branch `agent/v2.4.0-catalog-sync`, synchronized with the three local **2.3.0** catalog previews. `release_ref` remains null. Nothing was pushed or published.

## Synchronized catalogs

| Catalog | September (2.2.0) | October (2.3.0) |
|---|---|---|
| Biological Foundation Models | 400 | 486 |
| Autonomous Science Agents | 458 | 542 |
| AI Coding & Data Agents | 61 | 71 |

`python3 sync_catalogs.py --version 2.4.0 --date 2026-10-10` derived counts, versions, dates and SHA-256 checksums from the local child catalogs. It updated `catalog.json`, `child_catalogs.lock.json`, the standalone and embedded JSON-LD, the visible cards and the sitemap. The child catalogs' own audit notes record their evidence: `evidence/DISCOVERY_AUDIT_2026-10-10.md` (Foundation Models, Autonomous Agents) and `evidence/LIVE_AUDIT_2026-10-10.md` (Coding Agents).

## Checks

- `python3 -m unittest discover -s tests`: 11 tests pass.
- `python3 validate_portal.py`: pass against the sibling child catalogs; one expected warning for the null release reference.
- `validate_portal.py --remote` is expected to fail until the three child releases are published, because the live distributions are still the September files. Publish the children first, then re-run it.
- External links on the page (12): all HTTP 200, including bio.tools, which returned 521 in September. See `portal-link-audit-2026-10-10.json`.
- Browser review on a local HTTP server: portal and all three catalogs at 1440, 1024, 900 and 390 px. No document overflow and no console errors. The catalog tables keep the header aligned with the sticky controls above 900 px and switch to static controls with a horizontally scrolling table at 900 px and below. The Coding Agents search, reset, data-class selection, Free/academic filter and row expansion were exercised.
