# Open Implementation Gaps

## Scope

This file is the explicit gap register for `P00-T01`, especially `P00-T01-S03` in [`pm/backlog/phase-00-constraints-and-implementation-spec.md`](../../pm/backlog/phase-00-constraints-and-implementation-spec.md). Its purpose is to list implementation details that the current architecture names but does not fully specify, plus external open questions already tracked in [`pm/research/open-questions.md`](../../pm/research/open-questions.md).

This file is intentionally narrower than the PM workspace. It is not a roadmap, a phase plan, or a risk register. It is the unresolved-detail ledger that the implementation spec must either resolve or carry forward explicitly.

## Usage Rules

- This register is authoritative only for unresolved implementation detail discovery under `P00-T01`.
- A gap should move out of this file only when one of the following is true:
  - it is resolved in a formal implementation-spec document
  - it is converted into an explicit decision in `pm/07_decision_log.md`
  - it is converted into an externally owned open question with a clearly named owner and decision boundary
- "Safe local assumption" means a contributor may use it for local scaffolding or contract drafting only. It does not authorize release, production promotion, or policy-sensitive behavior.
- As of `2026-03-06`, the repository does not define calendar delivery dates for implementation work. Therefore "blocked-by date" is expressed as the earliest task or phase boundary by which the decision must exist. Where PM open questions already carry a task-bound deadline, that deadline is preserved here.

## Resolved During Phase 00 Baseline

The following gaps were resolved during the Phase 00 contract and engineering
baseline and therefore no longer remain in the active register:

- former `GAP-006`: the implementation-spec package structure is now fixed as a
  split implementation-doc set under `docs/implementation/`
- former `GAP-018`: the Python bootstrap is now normalized through `uv`,
  `uv.lock`, and `uv sync --dev`

## Register Fields

- `Gap ID`: stable identifier for the unresolved detail.
- `Type`: `internal` if the architecture leaves implementation detail open, `external` if the decision depends on an external governance or program input already tracked elsewhere.
- `Architecture Basis`: the relevant section or sections of `Architecture_Plan.md`.
- `Unresolved Detail`: the exact implementation question that still needs an answer.
- `Safe Local Assumption`: the narrowest assumption that can be used without hard-coding a future decision.
- `Blocked-By Boundary`: the last safe task or phase boundary before this gap becomes a blocker.
- `Affected Tasks`: the first tasks materially blocked or destabilized by deciding late.
- `Late-Decision Consequence`: the cost of leaving the gap unresolved too long.

## Cross-Cutting Gaps

### GAP-001 - Higher-environment deployment target remains unspecified

- Type: external
- Architecture Basis: Section 2, "Reference deployment and control plane"
- Related PM reference: `OQ-01`
- Unresolved Detail: the architecture specifies a self-managed Kubernetes deployment model. Local development is now narrowed to `kind` on Docker, but the actual higher-environment hosting target, storage-class shape, IAM surface, and network perimeter remain unresolved.
- Safe Local Assumption: use the internal-only `kind` target for local validation, keep Terraform modules provider-agnostic for higher environments, and do not mistake the local target for a shared-environment provider decision.
- Blocked-By Boundary: before provider-specific `P01-T02-S02` and before higher-environment `P01-T03` begins
- Affected Tasks:
  - provider-specific `P01-T02-S02`
  - higher-environment `P01-T03`
  - higher-environment `P01-T04`
- Late-Decision Consequence: Terraform modules, secret delivery, storage classes, DNS, ingress, backup paths, and service bootstrap will all incur rework if the hosting target is chosen after environment-specific implementation starts.

### GAP-002 - Budget and capacity envelope is not set

- Type: external
- Architecture Basis: Section 2 node pools, Section 4 heavy transform engine, Section 7 OCR fallback lanes
- Related PM reference: `OQ-02`
- Unresolved Detail: the architecture names GPU, stateful SSD, and CPU pools, but it does not set cost ceilings, storage growth assumptions, throughput targets, or acceptable dev vs pilot sizing.
- Safe Local Assumption: use the small-footprint local `kind` target for internal validation only, keep node-pool and storage-profile definitions logical rather than numeric for higher environments, and treat all performance observations as non-release-authoritative.
- Blocked-By Boundary: before capacity-sensitive `P01-T02-S02`, before `P01-T04`, and before production-scale `P02-T03`
- Affected Tasks:
  - capacity-sensitive `P01-T02-S02`
  - higher-environment `P01-T04`
  - production-scale `P02-T03`
- Late-Decision Consequence: node-pool design, OCR throughput, embedding throughput, retention policy, and pilot readiness claims will all be unstable or misleading.

### GAP-003 - Restricted-role governance authority is not fixed

- Type: external
- Architecture Basis: Sections 9, 13, 18, Part II sections 11, 12, and 16
- Related PM reference: `OQ-03`
- Unresolved Detail: the architecture requires restricted contexts, role-gated views, and stricter export than view policy, but it does not identify the approving authority for restricted roles, restricted routes, or export permissions.
- Safe Local Assumption: use deny-by-default behavior for restricted paths and keep all restricted features internal-only until governance is formalized.
- Blocked-By Boundary: before `P03-T02` promotion and before any restricted-feature preview
- Affected Tasks:
  - `P03-T02`
  - `P03-T03`
  - `P07-T04`
- Late-Decision Consequence: policy implementation may drift into an arbitrary local interpretation, creating later rework or unacceptable release risk.

### GAP-004 - Release audience and pilot cohort are undefined

- Type: external
- Architecture Basis: Part II overall, especially routes, review workbench, restricted features, and QA workspace
- Related PM reference: `OQ-04`
- Unresolved Detail: the architecture defines the application surfaces but not who the internal alpha, analyst preview, or restricted pilot users actually are.
- Safe Local Assumption: build for internal engineering and internal reviewer use only.
- Blocked-By Boundary: before `P06-T07`
- Affected Tasks:
  - `P06-T07`
  - `P07-T04`
- Late-Decision Consequence: route hardening, observability scope, documentation, onboarding, role testing, and release gates will be misaligned with the eventual audience.

### GAP-005 - Gold-set curation ownership is unresolved

- Type: external
- Architecture Basis: Sections 7, 14, 17; Part II section 17
- Related PM reference: `OQ-05`
- Unresolved Detail: the architecture requires gold sets for OCR, extraction, retrieval, and QA support evaluation, but it does not yet identify the owner who curates and signs them off.
- Safe Local Assumption: use provisional internal gold sets for experimentation only and mark them explicitly non-release-authoritative.
- Blocked-By Boundary: before `P05-T06`
- Affected Tasks:
  - `P05-T06`
  - `P07-T04`
- Late-Decision Consequence: threshold tuning remains anecdotal, and no later release gate can be defended rigorously.

### GAP-007 - Deterministic ID generation policy is not specified

- Type: internal
- Architecture Basis: Sections 5 and 8
- Unresolved Detail: the architecture names `document_id`, `page_id`, `span_id`, and `claim_id`, but it does not say how those identifiers are generated, whether they are deterministic across reprocessing, or how they behave when OCR or layout engines change.
- Safe Local Assumption: treat IDs as deterministic derivations from source lineage plus local position, and avoid introducing opaque random IDs into canonical contracts until the policy is formalized.
- Blocked-By Boundary: before `P00-T02-S01`
- Affected Tasks:
  - `P00-T02`
  - `P02-T04`
  - `P06-T04`
- Late-Decision Consequence: joins, lineage, rematerialization, and deep-linking may break across reruns.

### GAP-008 - Confidence semantics are not normalized across artifact types

- Type: internal
- Architecture Basis: Sections 7, 8, 11, 14, and Part II route behavior
- Unresolved Detail: the architecture uses confidence on OCR, spans, claims, events, and QA support, but it does not define whether confidence is probability-like, ordinal, calibrated, model-specific, or comparable across systems.
- Safe Local Assumption: store raw engine or model confidence separately from any normalized confidence field and do not compare them cross-pipeline until a formal normalization policy exists.
- Blocked-By Boundary: before `P00-T02-S03`
- Affected Tasks:
  - `P00-T02`
  - `P02-T03`
  - `P04-T04`
  - `P06-T05`
  - `P07-T02`
- Late-Decision Consequence: UI badges, review thresholds, and QA support labeling may imply false comparability.

### GAP-009 - Review-state lifecycle is not fully enumerated

- Type: internal
- Architecture Basis: Sections 1, 8, 14, 17; Part II sections 12 and 13
- Unresolved Detail: the architecture requires review states on many artifacts, but it does not specify the authoritative enum values, terminal states, re-open semantics, or which artifacts can inherit versus own review state.
- Safe Local Assumption: keep review-state handling explicit per artifact and avoid implicit inheritance until transitions are defined.
- Blocked-By Boundary: before `P00-T02-S03`
- Affected Tasks:
  - `P00-T02`
  - `P03-T04`
  - `P04-T02`
  - `P06-T06`
- Late-Decision Consequence: review queues, adjudication, rematerialization, and release gates will encode incompatible workflow semantics.

### GAP-010 - Promotion and rematerialization semantics are not fully specified

- Type: internal
- Architecture Basis: Sections 4, 16, and 17
- Unresolved Detail: the architecture is clear that derived assets are rematerialized rather than patched, but it does not yet specify exact trigger boundaries, invalidation order, or whether promotion is per-asset, per-batch, or per-branch.
- Safe Local Assumption: assume upstream accepted changes invalidate all directly dependent derived artifacts.
- Blocked-By Boundary: before `P01-T05-S01` and before `P03-T04-S03`
- Affected Tasks:
  - `P01-T05`
  - `P03-T04`
  - `P05-T02`
  - `P05-T01`
- Late-Decision Consequence: partial or stale analytical surfaces may survive after review outcomes or entity merges change.

## Platform, Control Plane, And Data Plane Gaps

### GAP-011 - Backup, restore, and recovery objectives are not specified

- Type: internal
- Architecture Basis: Section 2 off-cluster backups, Section 17 observability and lineage
- Unresolved Detail: the architecture says off-cluster backups exist, but it does not define recovery point objective, recovery time objective, backup frequency, or restore validation expectations for each store.
- Safe Local Assumption: document backup hooks for every stateful system and do not claim production readiness until restore drills exist.
- Blocked-By Boundary: before `P01-T04` production-oriented rollout and before `P07-T04`
- Affected Tasks:
  - `P01-T04`
  - `P07-T04`
- Late-Decision Consequence: production-readiness claims will be incomplete, and restore design may diverge across stores.

### GAP-012 - Higher-environment secret bootstrap and namespace segmentation are not fully specified

- Type: internal
- Architecture Basis: Section 2 secrets handling
- Unresolved Detail: the architecture specifies Vault and External Secrets. The Local-only baseline now defines operator namespace ownership, bootstrap token handling, and service-scoped secret materialization, but the higher-environment trust chain, auth backend, and final namespace tenancy model remain unresolved.
- Safe Local Assumption: use the Local control-plane baseline in `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`, keep runtime secrets service-scoped and namespace-scoped, and avoid cross-namespace sharing or higher-environment auth assumptions until policy is formalized.
- Blocked-By Boundary: before `P01-T03-S02`
- Affected Tasks:
  - `P01-T03`
  - `P01-T04`
  - `P01-T07`
- Late-Decision Consequence: Local work can continue safely, but higher-environment secret sprawl and inconsistent trust boundaries will be harder to correct after service rollout if the remaining auth and tenancy decisions are left vague.

### GAP-013 - Kafka topic taxonomy and retention policy are not specified

- Type: internal
- Architecture Basis: Section 4 event backbone, Section 19 end-to-end flow
- Unresolved Detail: the architecture now has a concrete integration-event inventory and schema-ownership model, but it still does not define concrete Kafka topic names, retention windows, replay rules, or partitioning strategy.
- Safe Local Assumption: use the published event inventory as the semantic baseline while keeping broker-level topic and retention assumptions out of code until Phase 01 eventing work begins.
- Blocked-By Boundary: before `P01-T05-S02`
- Affected Tasks:
  - `P01-T05`
  - `P02-T01`
  - `P03-T04`
- Late-Decision Consequence: event consumers may couple to unstable topic names or retention semantics, causing replay and lineage inconsistencies.

### GAP-014 - Model gateway provider matrix is not fixed

- Type: internal
- Architecture Basis: Section 4 model-serving control, Section 14 weak supervision, Part II section 12 QA
- Unresolved Detail: the architecture requires all model traffic to pass through a gateway, but it does not yet specify which vendors or self-hosted models are mandatory for baseline environments, nor which tasks may use which models.
- Safe Local Assumption: keep the gateway surface provider-agnostic and avoid embedding provider-specific capabilities into core contracts.
- Blocked-By Boundary: before `P01-T05-S03`
- Affected Tasks:
  - `P01-T05`
  - `P05-T05`
  - `P07-T01`
- Late-Decision Consequence: prompt contracts, cost assumptions, latency expectations, and evaluation baselines may all require refactoring.

### GAP-015 - Iceberg catalog migration decision boundary is not formalized

- Type: internal
- Architecture Basis: Section 3 Iceberg JDBC catalog with possible later REST migration
- Unresolved Detail: the architecture allows starting with JDBC and later switching to REST, but it does not specify what technical or operational signals would trigger that migration.
- Safe Local Assumption: design catalog-access abstractions so a later catalog backend can change without rewriting asset schemas.
- Blocked-By Boundary: before `P01-T04-S04`
- Affected Tasks:
  - `P01-T04`
  - `P02-T05`
  - `P05-T03`
- Late-Decision Consequence: catalog assumptions may get baked into ingestion and analytics code paths.

## Ingestion And Canonical Evidence Gaps

### GAP-016 - Official source allowlist and change-detection contract are not formalized

- Type: internal
- Architecture Basis: Section 5 harvester service
- Unresolved Detail: the architecture restricts harvesting to official DOJ pages and associated official URLs, but it does not yet define the machine-readable allowlist, canonical URL rules, redirect handling, or content-change detection policy.
- Safe Local Assumption: permit only DOJ-hosted URLs explicitly linked from known corpus pages and record every redirect without trusting it as canonical.
- Blocked-By Boundary: before `P02-T01-S01`
- Affected Tasks:
  - `P02-T01`
  - `P02-T05`
- Late-Decision Consequence: harvester behavior may drift, causing stale source coverage or accidental source-boundary expansion.

### GAP-017 - Archive explosion safety limits are not specified

- Type: internal
- Architecture Basis: Section 6 routing and recursive archive explosion
- Unresolved Detail: the architecture requires archives to be exploded recursively while preserving the original archive, but it does not define recursion depth, size ceilings, bomb protection, child-member naming, or partial-failure handling.
- Safe Local Assumption: preserve the archive object and treat child extraction as bounded, auditable, and fail-safe rather than best-effort recursive expansion.
- Blocked-By Boundary: before `P02-T02-S03`
- Affected Tasks:
  - `P02-T02`
  - `P02-T06`
- Late-Decision Consequence: unsafe input handling or inconsistent evidence lineage can emerge before review catches it.

### GAP-018 - Canonical duplicate representative selection policy is not specified

- Type: internal
- Architecture Basis: Section 6 deduplication
- Unresolved Detail: the architecture says duplicate sets keep one canonical representative but does not specify how that representative is chosen when variants differ in fidelity, OCR quality, attachment completeness, or provenance richness.
- Safe Local Assumption: preserve all members and avoid irreversible promotion logic until a canonical-selection policy exists.
- Blocked-By Boundary: before `P02-T02-S02`
- Affected Tasks:
  - `P02-T02`
  - `P02-T04`
  - `P05-T01`
- Late-Decision Consequence: search and downstream analytics may attach to a low-fidelity duplicate and later need expensive rematerialization.

### GAP-019 - OCR routing calibration plan is incomplete

- Type: internal
- Architecture Basis: Section 7 PDF, image, and layout processing
- Unresolved Detail: the architecture gives starting thresholds and a tiered OCR lane, but it does not yet specify the handwriting classifier choice, calibration dataset composition, failure escalation thresholds per document family, or re-estimation cadence.
- Safe Local Assumption: keep the lane order exactly as specified and record per-page raw metrics needed for later recalibration.
- Blocked-By Boundary: before `P02-T03-S04`
- Affected Tasks:
  - `P02-T03`
  - `P03-T04`
  - `P05-T06`
- Late-Decision Consequence: OCR quality may be too brittle for later extraction or review workloads, and the thresholds will be hard to defend.

### GAP-020 - Canonical layout and geometry payload format is not specified

- Type: internal
- Architecture Basis: Sections 7 and 8
- Unresolved Detail: the architecture requires page coordinates, bounding boxes, and layout JSON linkage, but it does not specify the canonical bbox format, coordinate normalization rules, or layout JSON schema.
- Safe Local Assumption: preserve original extractor geometry alongside any normalized representation and avoid lossy transformation until the canonical payload is defined.
- Blocked-By Boundary: before `P02-T04-S01`
- Affected Tasks:
  - `P02-T04`
  - `P06-T04`
  - `P07-T02`
- Late-Decision Consequence: overlay rendering, span linking, and citation highlighting may not remain stable across extractors.

### GAP-021 - Non-PDF media artifact schema is not specified

- Type: internal
- Architecture Basis: Sections 6 and 7 mention image, audio, video, and office documents, but the canonical evidence model example is PDF-centric
- Unresolved Detail: the architecture says the platform is multimodal, but it does not yet define how non-PDF images, videos, audio assets, or office documents map into the canonical evidence model and span-oriented downstream workflows.
- Safe Local Assumption: preserve raw media and manifest metadata without forcing them prematurely into PDF-derived page/span semantics.
- Blocked-By Boundary: before broadening `P02-T03` beyond PDF-first evidence cohorts
- Affected Tasks:
  - `P02-T03`
  - `P02-T04`
  - `P05-T01`
- Late-Decision Consequence: multimodal support may become inconsistent or bolted on, undermining the architecture’s stated scope.

## Policy, Review, And Security Gaps

### GAP-022 - Victim-sensitive recognizer governance is not specified

- Type: internal
- Architecture Basis: Section 9 sensitivity tagging, Section 13 redaction-safe analysis
- Unresolved Detail: the architecture requires allow or deny lists and custom recognizers for protected victim context, but it does not specify who maintains those lists, how they are versioned, or how updates propagate.
- Safe Local Assumption: treat any victim-sensitive recognizer extensions as centrally versioned policy artifacts, not local service config.
- Blocked-By Boundary: before `P03-T01-S02`
- Affected Tasks:
  - `P03-T01`
  - `P03-T03`
  - `P07-T03`
- Late-Decision Consequence: policy behavior may drift between environments or services, which is especially dangerous in restricted contexts.

### GAP-023 - Export approval workflow and artifact set are not specified

- Type: internal
- Architecture Basis: Sections 1, 13, 18; Part II sections 12 and 16
- Unresolved Detail: the architecture says exports are more restricted than views, but it does not define what export types exist, who approves them, what audit payload they require, or how partial versus raw exports differ.
- Safe Local Assumption: keep exports disabled except for internal engineering validation until a formal export matrix exists.
- Blocked-By Boundary: before `P03-T03-S04` and before `P06-T01-S02` exposes export routes
- Affected Tasks:
  - `P03-T03`
  - `P06-T01`
  - `P07-T04`
- Late-Decision Consequence: export implementation may accidentally over-permit raw evidence movement or miss required audit hooks.

### GAP-024 - Audit retention and access policy are not specified

- Type: internal
- Architecture Basis: Sections 17 and 18
- Unresolved Detail: the architecture requires audit logs but does not specify retention periods, log redaction rules, privileged readers, or whether audit data itself contains restricted context.
- Safe Local Assumption: log minimal necessary metadata for sensitive actions and treat audit access as more restricted than ordinary reviewer access.
- Blocked-By Boundary: before `P03-T05-S01`
- Affected Tasks:
  - `P03-T05`
  - `P07-T04`
- Late-Decision Consequence: audit implementation may either over-collect restricted context or under-collect actionable evidence for investigations.

### GAP-025 - Definition of "high-impact merge" is not specified

- Type: internal
- Architecture Basis: Sections 1 and 10
- Unresolved Detail: the architecture requires human adjudication for high-impact merges but does not define the exact criteria that make a merge high impact.
- Safe Local Assumption: classify ambiguous cross-thread, cross-contact-point, or high-degree-entity merges as review-required until a stricter definition exists.
- Blocked-By Boundary: before `P04-T02-S03`
- Affected Tasks:
  - `P04-T02`
  - `P03-T04`
- Late-Decision Consequence: merge automation may become too aggressive or too conservative, either way destabilizing graph and QA outputs.

## Semantics And Analytical Model Gaps

### GAP-026 - Final relation predicate catalog is not specified

- Type: internal
- Architecture Basis: Section 11 relation extraction
- Unresolved Detail: the architecture provides examples of relation predicates but does not define the canonical controlled vocabulary, aliasing rules, or deprecation policy for predicates.
- Safe Local Assumption: limit extraction to the explicitly named example predicates until the controlled vocabulary is approved.
- Blocked-By Boundary: before `P04-T03-S03`
- Affected Tasks:
  - `P04-T03`
  - `P05-T02`
  - `P06-T04`
- Late-Decision Consequence: graph schema, API contracts, and UI labels will diverge if predicates proliferate informally.

### GAP-027 - Event ontology detail and acceptance thresholds are not specified

- Type: internal
- Architecture Basis: Section 11 event extraction, Section 15 temporal analytics
- Unresolved Detail: the architecture names minimum event classes but does not define required versus optional fields per event type, event-confidence acceptance thresholds, or how uncertain intervals are normalized across event families.
- Safe Local Assumption: keep event schemas strict, sparse, and evidence-linked rather than filling implied fields.
- Blocked-By Boundary: before `P04-T04-S01`
- Affected Tasks:
  - `P04-T04`
  - `P05-T03`
  - `P06-T05`
- Late-Decision Consequence: event-derived timelines, graph edges, and QA evidence packs will not remain semantically consistent.

### GAP-028 - Event coreference merge policy is not specified

- Type: internal
- Architecture Basis: Section 11 cross-document event coreference
- Unresolved Detail: the architecture requires a second pass that merges mentions of the same underlying occurrence, but it does not define merge confidence policy, review triggers, or rollback semantics when event coreference is wrong.
- Safe Local Assumption: keep canonical-event merges conservative and retain all supporting mention links.
- Blocked-By Boundary: before `P04-T04-S04`
- Affected Tasks:
  - `P04-T04`
  - `P05-T02`
  - `P05-T03`
  - `P07-T01`
- Late-Decision Consequence: one wrong event merge can distort graph neighborhoods, timelines, and retrieval explanations.

### GAP-029 - Topic namespace governance is not specified

- Type: internal
- Architecture Basis: Section 12 topic modeling, Part II section 9 topic atlas
- Unresolved Detail: the architecture says per-family topics align into a higher-level namespace, but it does not define how that namespace is governed, versioned, renamed, or retired.
- Safe Local Assumption: keep topic labels provisional and preserve stable machine identifiers independent of human-readable labels.
- Blocked-By Boundary: before `P05-T04-S04`
- Affected Tasks:
  - `P05-T04`
  - `P07-T03`
- Late-Decision Consequence: topic atlas URLs, saved views, and longitudinal analytics may break when labels change.

### GAP-030 - Weak-label promotion rules are not fully specified

- Type: internal
- Architecture Basis: Section 14 weak supervision, Section 17 evaluation
- Unresolved Detail: the architecture requires probabilistic labels and calibration, but it does not yet define which labels may appear in analyst-facing views, which remain review-only, and which may never be exposed outside internal evaluation.
- Safe Local Assumption: treat all weak-label outputs as internal or review-only until a formal exposure policy exists.
- Blocked-By Boundary: before `P05-T05-S04`
- Affected Tasks:
  - `P05-T05`
  - `P07-T03`
  - `P07-T01`
- Late-Decision Consequence: model-derived labels may leak into product surfaces before their trust boundary is agreed.

## Retrieval, BFF, UI, And QA Gaps

### GAP-031 - Retrieval artifact storage contract is not fully specified

- Type: internal
- Architecture Basis: Section 16 retrieval artifacts, Part II section 5 search
- Unresolved Detail: the architecture names multiple retrieval artifact classes, but it does not define the exact storage contract, source-of-truth linkage fields, refresh cadence, or whether every artifact class is mandatory at MVP.
- Safe Local Assumption: start with the minimum artifact classes needed for the evidence workbench and keep refresh metadata explicit.
- Blocked-By Boundary: before `P05-T01-S01`
- Affected Tasks:
  - `P05-T01`
  - `P06-T03`
  - `P07-T01`
- Late-Decision Consequence: search behavior and explanation payloads may drift as new artifact classes are added ad hoc.

### GAP-032 - BFF persistence model for jobs and exports is not specified

- Type: internal
- Architecture Basis: Part II sections 3, 14, and 15
- Unresolved Detail: the architecture names job and export endpoints, but it does not define the authoritative job store, job lifecycle states, export metadata shape, or idempotency semantics.
- Safe Local Assumption: treat jobs and exports as explicit operational records with immutable status transitions rather than in-memory workflow state.
- Blocked-By Boundary: before `P06-T01-S02`
- Affected Tasks:
  - `P06-T01`
  - `P06-T06`
  - `P07-T04`
- Late-Decision Consequence: UI polling, retries, and auditability will be unstable.

### GAP-033 - Saved-search and saved-analytics persistence contract is not specified

- Type: internal
- Architecture Basis: Part II sections 4 and 14
- Unresolved Detail: the architecture says analyst work can be bookmarked, exported, or saved, but it does not specify how saved search state, saved filters, or dashboard definitions are persisted and versioned.
- Safe Local Assumption: keep saved-state contracts explicit and separate from browser-local cache assumptions.
- Blocked-By Boundary: before `P06-T02-S04` and before `P07-T03-S03`
- Affected Tasks:
  - `P06-T02`
  - `P07-T03`
- Late-Decision Consequence: saved work may become non-reproducible or silently incompatible across route changes.

### GAP-034 - Graph query limits and subgraph budgeting are not specified

- Type: internal
- Architecture Basis: Part II section 10 graph explorer
- Unresolved Detail: the architecture requires bounded subgraphs but does not define default hop limits, node or edge caps, timeout handling, or degraded-result behavior.
- Safe Local Assumption: keep graph queries bounded conservatively and return explicit truncation metadata rather than silently expanding.
- Blocked-By Boundary: before `P05-T02-S03` and before `P07-T03-S01`
- Affected Tasks:
  - `P05-T02`
  - `P07-T03`
- Late-Decision Consequence: graph UX may become unusable or operationally expensive before safe limits are agreed.

### GAP-035 - Citation granularity and QA evidence-pack persistence are not specified

- Type: internal
- Architecture Basis: Part II section 12 QA workspace, Section 17 lineage and observability
- Unresolved Detail: the architecture requires citation rendering and evidence-pack inspection, but it does not define whether citations anchor at span, block, or page level by default, nor how evidence packs are stored for audit and replay.
- Safe Local Assumption: anchor citations to the smallest available evidence-backed span and preserve the enclosing page reference.
- Blocked-By Boundary: before `P07-T01-S02` and before `P07-T02-S03`
- Affected Tasks:
  - `P07-T01`
  - `P07-T02`
- Late-Decision Consequence: QA answers may not be replayable or navigable in a consistent way.

### GAP-036 - Prompt-log retention and restricted-content handling are not specified

- Type: internal
- Architecture Basis: Sections 3, 14, 17; Part II section 12
- Unresolved Detail: the architecture says prompt logs exist and QA remains policy-bounded, but it does not define what parts of prompts, evidence packs, or model outputs are retained, how they are redacted, or who may read them.
- Safe Local Assumption: log only the minimum metadata required for audit until a prompt-log policy is specified.
- Blocked-By Boundary: before `P07-T01-S03`
- Affected Tasks:
  - `P07-T01`
  - `P03-T05`
  - `P07-T04`
- Late-Decision Consequence: prompt logging may either violate policy or be too thin to support incident review.

## Remaining High-Priority Gaps After Phase 00 Baseline

The following unresolved items remain the highest-value follow-on targets after
the completed Phase 00 baseline:

1. Deterministic ID generation plus confidence and review-state normalization:
   `GAP-007`, `GAP-008`, and `GAP-009`.
2. Promotion, rematerialization, and broker-level eventing detail:
   `GAP-010` and `GAP-013`.
3. Policy governance details that still depend on `OQ-03`, especially
   recognizer governance, export approval workflow, and audit retention:
   `GAP-022`, `GAP-023`, and `GAP-024`.
4. Phase 06 and Phase 07 interaction-surface gaps around BFF persistence,
   saved analytics, citations, and prompt-log handling:
   `GAP-032`, `GAP-033`, `GAP-035`, and `GAP-036`.
5. A decision intake pass on `OQ-01` through `OQ-05` so Phase 01 does not
   inherit unresolved program-level blockers silently.

## Source Basis

- Local architecture source: [`Architecture_Plan.md`](../../Architecture_Plan.md)
- PM open-question source: [`pm/research/open-questions.md`](../../pm/research/open-questions.md)
- Related task definition: [`pm/backlog/phase-00-constraints-and-implementation-spec.md`](../../pm/backlog/phase-00-constraints-and-implementation-spec.md)
