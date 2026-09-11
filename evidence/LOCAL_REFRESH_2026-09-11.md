# September 11 local review candidate

> Historical local-review snapshot. The owner subsequently authorized publication; see [release packaging](RELEASE_2026-09-11.md).

The three indexes and their parent portal are updated locally. Nothing has been
committed, pushed, tagged, released or deployed. This report describes the review
candidate; it does not represent a published release.

| Catalog | Previous | Candidate | Main change |
|---|---:|---:|---|
| Biological Foundation Models | 390 | 400 | 11 additions/promotions; GPN-MSA correction; ALICE held |
| Autonomous Science Agents | 438 | 458 | 21 additions; six existing corrections; Periodic Labs held |
| Coding & Data Agents | 60 | 61 | All 59 retained rows reviewed and updated; Pi and Zencoder added; Nobie held |

All child candidates are version 2.2.0; the portal candidate is 2.3.0. Their
modification date is September 11, 2026. Stable IDs and prior evidence are
preserved, including snapshots and restoration conditions for held records.

## Review coverage

Foundation discovery covered all ten modalities and reconsidered all 39 previous
holds; 44 candidates now remain held. The autonomous-agent refresh covered the
five domain/benchmark lanes, current artifact access and selected older claims.
These two catalogs preserve older verification dates for claims that were not
fully re-reviewed. All 61 coding-tool public summaries were reviewed against
current first-party evidence and carry September 11 verification dates.

Independent cross-reviews checked model artifacts/licences, agent scope and
autonomy, and coding-tool plan, inference, telemetry and storage boundaries.
Corrections include Modelica sample-data restrictions, ARCHE's partial release,
Kiro's stored service content, Ante's log export, and Replit's Enterprise terms.
Zerve now uses an explicit `unknown` data-handling value (shown as **Unclear**)
instead of implying proven training or retention behavior. Its special-category
recommendation remains `no`. No pure-cloud special-category route was admitted.

Source inspection is not execution of the indexed software, reproduction of
scientific results, or institutional approval. Access restrictions and
unpublished contractual details remain qualified in the records.

## Validation

- Child migrations are idempotent; generated distributions build deterministically.
- Full schemas, identity/date invariants and preview checks pass.
- Portal synchronization uses local child files and binds cards to their IDs;
  eleven regression tests pass, including two independently reproduced defects
  that were fixed during review.
- Current displayed-catalog URL coverage: Foundation 1,005 URLs (198 restricted),
  Autonomous 819 (30 restricted), Coding 397 (24 restricted). No current audited
  catalog URL is classified as missing or a network/server failure. The original
  ALICE failure remains in evidence alongside the reversible hold.
- Search, each available filter, reset, keyboard row expansion/collapse and the
  coding data-class states were checked in Chrome. Desktop and mobile geometry
  were measured at 1440, 1024, 900 and 390 pixels. Results are recorded in
  `browser-review-2026-09-11.json`; screenshots are kept locally.
- The live public JSON files still contain the previous 390/438/60 records and
  baseline checksums. A remote comparison therefore correctly fails against the
  new local lock. Release checks fail solely because release references remain
  intentionally null.

The related **bio.tools** site currently returns HTTP 521. Its canonical link
is retained and its verification date was not advanced. This upstream failure
is separate from the child-catalog URL results above.

## Evidence and publication boundary

`final-catalog-summary-2026-09-11.json` records exact local data hashes and changed
IDs. `CROSS_CATALOG_REVIEW_2026-09-11.md` records coordinator source checks and
adjudications. Each child repository contains its dated discovery/live audit,
compact source evidence and reviewed migration.

Navigator and Trial Agent projects were not updated. Their data-handling
consumers were inspected read-only for compatibility with the new `unknown`
value.

Next comes owner review of the local candidate. Only after agreement: set the
planned immutable release references, rerun release checks, commit/package and
publish the child catalogs, synchronize the portal against the actual published
bytes, then publish and verify the portal. Publication remains the final step.
