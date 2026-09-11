# Local integration and second review — 2026-09-11

> Historical local-review snapshot. The owner subsequently authorized publication; see [release packaging](RELEASE_2026-09-11.md).

Status: complete for local owner review. This note distinguishes coordinator source checks from delegated catalog review and automated validation. No publication is authorized in this refresh; all changes remain local.

## Frozen baseline

See `refresh-baseline-2026-09-11.json` for the four repository HEADs and canonical-data SHA-256 values. Starting counts: 390 foundation-model records, 438 autonomous-agent records, 60 coding/data tools; 39 foundation-model candidates held separately. Local HEADs matched public `main` before editing.

## Source checks and editorial adjudication

The coordinator reopened the following primary sources instead of relying only on the catalog agent's summaries:

- **ToolUniverse** — [README](https://github.com/mims-harvard/ToolUniverse/blob/main/README.md), blob `9bfe1def9fe70caa0450953c893803fe62cd5899`. The project exposes scientific tools and explicit sequential/parallel tool composition. Retain the existing selected infrastructure entry with its dependency on an agent clear; do not infer autonomous scientific closure from the library alone.
- **ChemMCP** — [README](https://github.com/OSU-NLP-Group/ChemMCP/blob/main/README.md), blob `d22f335b88a7b5fbcbc682edcf7fd83d85863914`. Native multi-turn RL agent loops are now documented alongside the toolkit; its disclaimer still distinguishes it from a standalone agent. Retain, with that distinction visible.
- **PUDA** — [README](https://github.com/PUDAP/puda/blob/main/README.md), blob `dc190639dbfaa504d321aef9cfaccda3ecaec053`. The documented system separates drivers, communication, orchestration, and agent-issued commands. Retain the existing hardware-harness entry, clarify that scientific reasoning/autonomy depends on the configured agent workflow.
- **K-Dense scientific-agent-skills** — [README](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/README.md), blob `ffe74446e47f2470be3997bc20aa4e4a8ebbb283`. Repository MIT terms do not establish a common licence for every skill; the README explicitly identifies separately licensed skill content. A new paper is linked. Retain this deliberate August inclusion, correct licence wording and paper metadata after the catalog lane checks the paper. Avoid an exact skill count because different repository sections disagree.

The catalog lane initially proposed removing these four as components. The coordinator retained them: August explicitly admitted selected scientific-agent infrastructure, and the protocol's statement that this is not a general component directory does not unambiguously revoke those decisions. This refresh does not broaden the inclusion policy. The distinction between infrastructure and standalone systems remains an editorial taxonomy issue; no blanket scope purge is applied.

- **Zerve** — [pricing and deployment FAQ](https://www.zerve.ai/pricing), primary HTML checked 2026-09-11. The page markets enterprise on-premises/air-gapped platform deployment but lists OpenAI and Anthropic as supported BYOK providers; self-hosted models are request-only. Platform hosting alone does not demonstrate in-boundary model inference. This supports the proposed conservative special-category downgrade until that route is documented. The same page contains conflicting free-credit amounts, which should remain qualified rather than chosen arbitrarily.
- **Kiro** — [data protection](https://kiro.dev/docs/privacy-and-security/data-protection/), primary HTML checked 2026-09-11. Service content can be stored, including for logging/reporting; enterprise content is excluded from service improvement. No-training and no-storage are distinct, supporting removal of the old blanket no-storage claim.
- **Nobie** — [README](https://github.com/nobie-org/nobie-cli/blob/main/README.md), blob `16e7ceee87c108379fe01808929b2d0855118a07`. It documents a workbook execution engine and external coding-agent integration; this does not prove a local inference boundary or an independent autonomous data agent. Suitability must be based on the complete workflow.

These were primary page/repository text checks. They are not execution tests, legal approvals, or validation of claimed scientific performance. The final integrated row text and rendered classifications were checked against these findings.

## Further coordinator findings

- **Periodic Labs** — [official site](https://periodic.com/), primary HTML reopened 2026-09-11. The cited material describes an AI-scientist development goal and custom agent work with industry. It does not support the displayed claim of observed A5 physical autonomy. Move the displayed row to a reversible evidence hold, preserving its full prior content and stable ID. This is an evidence decision, not a statement that the company is discontinued; do not invent a lower autonomy level in place of the unsupported one.
- **Benchmark-as-Teacher** — [primary preprint](https://arxiv.org/abs/2608.16211) and [README](https://github.com/AutoMedBench/Benchmark-as-Teacher/blob/main/README.md), blob `1f0ec5706da3ef606d003fb92323029dc203d3f0`. The candidate row describes the recursive training/evaluation framework, whose outputs are policies and curriculum/evaluation artifacts. Classify that entry as a benchmark/evaluation-training harness (B), rather than inferring A4 research autonomy from the training feedback loop. A separate concrete agent entry would require evidence for its own released execution route.

## Shuffled sample of new records

- **EarthVerse** — the primary [preprint](https://arxiv.org/abs/2608.23525) and [README](https://github.com/CuiZHIQ/Earth-Verse/blob/main/README.md), blob `ad6ad8f2f238c5aa63489aa1fbef88b53170edce`, support benchmark classification, package-scoped investigations and the released evaluation materials. The row distinguishes software, task and upstream evidence terms.
- **ARCHE** — [preprint abstract](https://arxiv.org/abs/2609.11147) and [README](https://github.com/JetAstra/Arche-Harness/blob/main/README.md), blob `882c6b083dcd7f96005358acd7925bc2d6c8737d`. The current harness differs from the paper implementation and omits the paper-specific chemistry weights, reward model and training pipeline. Requested a visible partial-reproduction qualification; source availability must not imply the evaluated system can be fully reproduced from this snapshot.
- **Modelica Agent Workflow Benchmark** — [preprint](https://arxiv.org/abs/2608.23653) and [README](https://github.com/wangzizhe/modelica-agent-workflow-benchmark/blob/main/README.md), blob `b8b0481fd3bb8b11b4c4a92293d7f28367b13d04`. The initial new row omitted the separate sample-data licence restricting model training, fine-tuning and distillation. Requested correction of its access category, licence evidence and visible note, while preserving the distinction between public demos and private official evaluation.
- **OmniScientist (omni-modal)** — [preprint](https://arxiv.org/abs/2608.13558) and [README](https://github.com/Omni-Scientist/OmniScientist/blob/main/README.md), blob `0c8f95b9c7817b6ffe7c8d6f609ec6911aa99f05`, agree with the computational-loop description and the desktop release replacing the discontinued standalone CLI. The row distinguishes its identity from the older namesake.
- **RIBOSPAN** — reopened the [model licence](https://huggingface.co/SII-GAIR-NLP/RIBOSPAN-FM/blob/main/LICENSE) using its raw-text endpoint when the web reader failed. Sections 1–3 distinguish Apache code from noncommercial model materials and extend the commercial-use restriction to outputs and output-derived models. The row preserves this distinction.
- **NucleicBERT** — [Zenodo record](https://zenodo.org/records/16989562) and public record API show the base `pretrained.pt` plus separate task checkpoints and `apache2.0` licence metadata. This supports the archive-access claim without downloading or executing checkpoints.
- **MultiFlow** — [Zenodo record](https://zenodo.org/records/10714631), read through its public API after a web-reader timeout, lists a 239,550,153-byte `weights.tar.gz` and datasets under CC BY 4.0. The row correctly distinguishes archive terms from MIT code.
- **GPN-Star** — the [human vertebrate model card](https://huggingface.co/songlab/gpn-star-hg38-v100-200m) declares MIT and shows safetensors. Its prose card is empty; the project paper/repository, rather than this empty card, must support biological and inference claims.
- **MicroGenomer** — [official README](https://github.com/BGIResearch/MicroGenomer/blob/main/README.md), blob `5c11dc69fdf3918b7b7d7001c09f237a5347b54a`, links the author-hosted 470M checkpoint and documents genome-labelled coding-sequence inputs, embedding extraction and six downstream tasks. The row reflects this scope.
- **MultiFlow and GPN follow-up** — MultiFlow's [README](https://github.com/jasonkyuyim/multiflow/blob/main/README.md), blob `855379851550d16d1e3a8dfd595dde6c146c72b9`, documents co-design, inverse folding and forward folding configurations. The [GPN README](https://github.com/songlab-cal/gpn/blob/main/README.md), blob `4778b53c001717d76af078e527a71d0d41e4d7ea`, supports the GPN-MSA deprecation and the distinction between alignment-dependent inference and other family members.
- **LAMBDA** — [README](https://github.com/leannmlindsey/LAMBDA/blob/main/README.md), blob `2a6363f51c2a6dfbed63cd43e610eac942c5e566`, supports a reusable genomic-model benchmark. Requested an additional qualification that non-EVO2 fine-tuned task checkpoints are available from the authors on request; the public archive contains the small EVO2 probe heads and an upstream-model pointer.

## Portal maintenance changes

Local validation now resolves sibling child checkouts before the historical `repos/` layout. It compares child bytes/counts and resource identity/version/date with the lock. The remote mode still forces the live public files; standalone clones still validate against the saved lock.

`sync_catalogs.py` regenerates collection summaries, visible counts/date badges, embedded/standalone JSON-LD, checksums and sitemap dates from local children. It leaves the immutable release reference unset and makes no network writes. Regression tests cover both layouts, the standalone fallback, same-count content drift, version/date drift, remote behavior, invalid calendar dates, and repeatable synchronization without copying child records into the portal.

## Independent cross-reviews and final adjudication

The autonomous-agent reviewer independently checked PlantRNA-FM, Monroe,
FrameFlow, Mol-JEPA, KinConfBench and the ScDiVa hold against primary sources.
PlantRNA-FM's downstream predictions were clarified as requiring fine-tuning;
ScDiVa's fallback emits a warning rather than failing silently. Both edits were
reread. The review's KinConfBench publisher-access limit is preserved in
`Autonomous_Agents/evidence/refresh-2026-09-11/foundation-cross-review.md` and
its concise source registry. No admission blocker remained in that sample.

The foundation-model reviewer independently checked Pi, Zencoder, Ante,
Kiro/CLI, Amp, Replit and DataFoundry. It confirmed the conditional inference
routes, storage/telemetry distinctions and plan limits and requested precise
Amp retention wording, which was applied. The coordinator also reopened
Zencoder's [private deployment](https://docs.zencoder.ai/features/private-deployments)
and [custom model](https://docs.zencoder.ai/clis/custom-agent) documentation.
These describe customer-operated inference and hiding managed providers;
they do not establish default hosted-service zero storage.

DataFoundry was retained as one product after the coordinator checked the
parent [README](https://github.com/datagallery-ai/dataagent/blob/datafoundry/README.md),
blob `bd31b67b5f5352467af8cc23443b4015bc7ac79f`, and repository metadata. The
parent itself names DataFoundry and directs installation to the existing
distribution repository. Matching documentation is not evidence of an
independently marketed thin-fork duplicate, nor of every code file being
identical. Its early maturity and unfinished semantic-layer roadmap remain
qualified. Nobie was held under the coding catalog's existing off-the-shelf
scope, preserving its prior row and ID. ALICE's current source failures were
also preserved with its Foundation hold; neither hold asserts discontinuation.

## Completed integration gates

- Final counts: **400 / 458 / 61**, with all child versions **2.2.0** and portal
  version **2.3.0**, modified **2026-09-11**. Exact hashes and changed IDs are in
  `final-catalog-summary-2026-09-11.json`.
- The coordinator's final preview validators pass in all four repositories:
  **zero errors**, with only the intentionally unresolved release reference
  warning in each. Child deterministic/schema/identity/date/migration checks
  and the Foundation/Coding fault simulations passed in their maintenance runs.
  All four final `git diff --check` commands pass.
- The portal's **11 regression tests** pass. Independent review reproduced
  and then verified fixes for positional card misassignment and invalid child
  metadata overwriting outputs. Synchronization was repeated and produced
  byte-identical output.
- Browser review passed **57 available filter states**, search/reset and
  keyboard row expansion/collapse. All three coding sensitivity states were
  checked, with 0/4/28 dimmed rows agreeing with the canonical suitability
  data. The Unclear filter returns only Zerve; Pi/Zencoder display conditional
  routes, Clusy displays scoped no-training with no sensitive-data route, and
  Nobie is absent from the displayed table.
- At **1440, 1024, 900 and 390 pixels**, all pages fit the document width.
  Foundation/Autonomous headers align with sticky controls above 900 pixels
  and become static below that threshold. Coding preserves its static table
  header and horizontal mobile table. Portal card identities, dates, counts,
  loaded logos and keyboard skip link were checked. No page-script errors
  occurred. See `browser-review-2026-09-11.json`; viewport images were inspected
  locally using headless Chrome after the headed session timed out on capture.
- Active child URL audits have no missing/network/server failures; restricted
  sources remain qualified. The portal's 15 HTTP link targets have 14 reachable
  results and the documented bio.tools HTTP 521 failure. No verification date
  was advanced for that failed source.
- Strict release validation fails solely for the null release references.
  A forced remote portal comparison returns the old public **390 / 438 / 60**
  data and baseline hashes; its mismatch with this local candidate is expected.
  No online write, commit, tag, release or deployment was performed.
