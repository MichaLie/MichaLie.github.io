# Portal maintenance

The portal is a router over three independently maintained catalogs. This document is the canonical, tool-neutral protocol for humans and coding agents.

## Source-of-truth boundary

The child catalogs own their records. The portal owns only collection-level identity, routing, related-resource links, and synchronized summaries. Never copy individual model, agent, or tool records into this repository.

After any child release, update the matching `record_count` and `version` in `catalog.json`, mirror the change in `metadata.jsonld` and the embedded JSON-LD and visible card in `index.html`, and update `child_catalogs.lock.json` with the canonical distribution's exact SHA-256. The validator reads protected local child catalogs when they are available; in a standalone public fork it checks the versioned lock. `--remote` compares that lock with the fixed public JSON distribution URLs.

Related community or infrastructure resources belong in `related_resources`, `dct:relation`, `schema:relatedLink`, and the visible ecosystem section. They are not child catalogs, must carry `included_in_child_catalog:false`, and must never change the three catalog counts or `schema:numberOfItems: 3`.

## Required local gate

```bash
python3 -m pip install -r requirements-maintenance.txt
python3 validate_portal.py
python3 validate_portal.py --remote
python3 validate_portal.py --release
```

Then serve the repository over HTTP and review the desktop and mobile layouts, keyboard focus, all visible links, logos, and browser console. Do not use `file://` as the final browser test.

`validate_portal.py --remote` forces a fresh comparison with the three public JSON distributions even when protected local child catalogs exist. Before publication this gate is expected to fail while the older public distributions are still live. Publish and verify the child sites first, rerun the remote gate, and publish the portal last.

## Version and release reference

Use semantic versions for collection releases. During ordinary work, `release_ref` may remain null. During explicitly authorized final packaging it must match:

```text
<repository>/releases/tag/v<version>
```

The strict validator checks that relationship but does not create or publish the tag. After publication and before announcement, verify that the exact release URL resolves. No DOI is planned at this stage.

## FAIR and governance boundary

Keep the persistent identifier, version, publisher, licences, provenance, machine-readable metadata, schema, and human-readable page aligned. Catalog data, collection metadata, and original documentation are CC BY 4.0; validation and maintenance code are MIT. External resources, logos, and trademarks retain their own terms.

Michaela Liegertová is the individual curator and publisher. IMG CAS is affiliation only, and ELIXIR-CZ is dedication and community context only. Neither role implies institutional publication authority or endorsement.

FAIR validation is evidence about metadata and access, not certification of scientific validity, security, legal suitability, institutional approval, or continued availability of external resources.

## Publication boundary

Validation does not publish anything. Pushes, merges, Pages changes, tags, releases, DOI actions, and public announcements require explicit human authorization after the complete candidate has been reviewed. A fork must replace identity, publisher, licence, and provenance claims with values it is authorized to make.
