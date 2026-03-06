# Architecture Constraints

This document translates the architecture into implementation constraints that are mandatory for every phase, task, and subtask. No contributor may override these constraints without an explicit decision-log entry that changes the plan.

## Constraint AC-01: Lawful Source Boundary

- Only lawfully released public material and metadata derived from that material may enter the system.
- External enrichment sources must be approved explicitly before use.
- Harvester seeds are limited to official DOJ corpus pages and associated official URLs unless a later decision log expands the source boundary.

## Constraint AC-02: No Deanonymization

- The platform must never treat redactions as puzzles to solve.
- No task may infer, reconstruct, export, or operationalize protected victim identity.
- Any workflow that could materially facilitate deanonymization is prohibited.

## Constraint AC-03: Evidence Before Inference

- The primary truth object is the evidence-backed span.
- Summaries, embeddings, topic labels, clusters, graphs, and QA responses are derived artifacts, not evidence.
- UI and APIs must preserve this distinction in naming, storage, and review state.

## Constraint AC-04: Mandatory Provenance

Every derived artifact must carry enough metadata to reproduce its lineage. At minimum:

- source URL
- fetch timestamp
- SHA-256
- lakeFS commit
- Iceberg snapshot identifier
- extractor version
- model version when applicable
- page reference or coordinates or offsets
- timestamp of materialization
- review state

An artifact that cannot provide its provenance tuple is invalid and must not be promoted.

## Constraint AC-05: Layer Separation

The platform must preserve four logical layers:

1. raw evidence
2. extracted claims
3. inferred hypotheses
4. user interaction

Storage, APIs, UI labels, and review states must not blur those layers.

## Constraint AC-06: No Person-Level Risk Scoring

- Risk scoring may apply to passages, events, document clusters, or workflow states.
- Risk scoring may not apply directly to people.
- Labels and model outputs must remain non-accusatory and evidence-tethered.

## Constraint AC-07: Human Adjudication For High-Impact Actions

The following require human review before promotion:

- high-impact entity merges
- sensitive label acceptance
- policy-sensitive exports
- unresolved OCR cases that affect evidence usability
- QA outputs that fail support verification but could still influence analysis

## Constraint AC-08: QA Abstention

- QA must abstain when support is weak, contradictory, or blocked by policy.
- Evidence packs must remain viewable even when answer generation abstains.
- Support state must be explicit in the API and UI.

## Constraint AC-09: Browser Is Untrusted For Privileged Access

- The browser never queries OpenSearch, Neo4j, Trino, PostgreSQL, lakeFS, or model providers directly.
- All privileged data access flows through a backend-for-frontend with policy enforcement.
- Signed object URLs must be short-lived and scope-limited.

## Constraint AC-10: Policy Before Higher-Level NLP

- Sensitivity labeling runs before broad indexing, summarization, QA prompting, or unrestricted embedding.
- Restricted spans may exist in evidence storage but must be filtered from broad analyst surfaces unless role policy permits access.

## Constraint AC-11: Event-Centric Semantics

- The graph must be constructed from claims and events, not raw co-mention alone.
- Timeline analytics must be based on event tables, not undifferentiated documents.
- Entity timelines distinguish raw mentions from evidence-backed event participation.

## Constraint AC-12: Redactions Are First-Class Objects

- Redactions must be modeled explicitly.
- Broad-access indices may only contain masked or hashed local context where required.
- Redaction adjacency export is disabled for normal roles.

## Constraint AC-13: Deterministic Ingest And Replay

- Every ingest batch runs on an explicit lakeFS branch.
- Raw objects are never modified in place.
- Failed validation branches are retained for audit.
- The system must be able to replay downstream assets from a known ingest state.

## Constraint AC-14: Extraction Honesty

- The product must preserve image, native text, and OCR renderings when the source warrants it.
- Extraction-mode ambiguity must be visible to analysts.
- Confidence, rendering defects, and fragmentary reconstructions must be explicit rather than hidden.

## Constraint AC-15: Defense In Depth

- Authentication, application policy, and datastore-level filtering must align.
- OpenSearch DLS is not sufficient for protecting write paths.
- Operational writes to privileged stores must remain behind trusted services and service accounts.

## Constraint AC-16: Versioned Derived Assets

- Retrieval artifacts, graph projections, topic models, community summaries, and QA evidence packs are versioned derived assets.
- When an upstream merge or adjudication changes, dependent assets are rematerialized, not patched informally.

## Constraint AC-17: Test And Evaluation Gates Are Release Blockers

- A feature is not complete when code exists; it is complete when the relevant validation, evaluation, policy, and observability gates pass.
- Model-assisted features require corpus-specific evaluation and thresholding.

## Constraint AC-18: Implementation Must Remain Inspectable

- Search ranking, graph edges, QA answers, timeline intervals, and review decisions must expose why the system produced them.
- Hidden heuristics are allowed internally, but analyst-visible outputs must retain inspectable rationale and citation paths.

## Prohibited Shortcuts

The following shortcuts are explicitly disallowed:

- storing only chunks and embeddings without span-level evidence records
- indexing restricted spans into broad-access search by default
- exposing unrestricted redaction-neighbor context in QA prompts
- merging entities automatically into canonical identities without review pathways
- presenting inferred relationships as equivalent to evidence-backed relationships
- shipping a chat interface before citations, support verification, and abstention logic exist
- omitting review-state fields from derived objects
- letting UI code infer policy context client-side without server-provided policy state

## Enforcement Expectation

Every phase backlog file under [`backlog/`](./backlog) must reference these constraints. If an implementation task cannot satisfy a constraint yet, that task remains blocked or flagged as research-only until the gap is closed.

## References

- [`Architecture_Plan.md`](../Architecture_Plan.md): lines 1-20, 64-74, 89-109, 127-171, 187-243, 251-287, 295-297, 413-454, 466-470
- Official source support is cataloged in [`08_research_register.md`](./08_research_register.md)
