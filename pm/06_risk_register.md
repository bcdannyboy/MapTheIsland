# Risk Register

Status values: `active`, `watch`, `retired`

## Operational Risk Metadata

This register remains narrative by risk, but the following operational fields are required when risks are reviewed:

- owner role
- detection signal
- review cadence
- contingency trigger threshold
- residual risk after mitigation
- last reviewed date

Until named owners are assigned, use the owner archetypes from [`21_roles_and_responsibilities.md`](./21_roles_and_responsibilities.md).

## Risk Operations Matrix

| Risk ID | Provisional Owner Role | Detection Signal | Review Cadence | Contingency Trigger | Residual Risk Baseline | Last Reviewed |
| --- | --- | --- | --- | --- | --- | --- |
| R-01 | policy and security lead | policy test failures, unexpected restricted content in search or QA | weekly and before any release candidate | one confirmed leakage path or repeated policy-test failure | medium until enforcement is proven | 2026-03-06 |
| R-02 | architecture lead | missing provenance fields, lineage validation failures | weekly | any promoted artifact missing mandatory provenance | medium | 2026-03-06 |
| R-03 | document-processing lead | low OCR confidence, review queue growth, analyst complaints | weekly | sustained low-confidence cohorts or unusable difficult-page rate | high until gold-set calibration exists | 2026-03-06 |
| R-04 | semantics lead | merge-review rejects, identity rollback requests | weekly | one confirmed harmful merge or elevated false-merge rate | medium | 2026-03-06 |
| R-05 | policy and security lead | unauthorized write-path design or service-account misuse | weekly and before search release | any evidence that write paths depend on DLS alone | medium | 2026-03-06 |
| R-06 | retrieval, graph, and analytics lead | graph validation failures, analyst complaints about noisy edges | weekly | graph views show unqualified co-mention as default evidence | medium | 2026-03-06 |
| R-07 | application lead | QA regression failures, support-state failures | weekly and before QA preview | one verified unsupported answer in preview path | medium | 2026-03-06 |
| R-08 | program manager | dashboard churn, backlog growth, milestone slippage | weekly | MVP-critical work loses priority to non-critical scope | high | 2026-03-06 |
| R-09 | platform or infrastructure lead | service instability, failed reconciliations, unrecoverable drift | weekly | repeated stateful service instability or failed restore path | medium | 2026-03-06 |
| R-10 | release lead | missing gold sets, threshold debates without evidence | weekly | promotion decisions depend on anecdotal confidence only | high | 2026-03-06 |
| R-11 | application lead | UI rework due to shifting contracts, missing response fields | weekly | frontend work blocked or redone because contracts were implicit | medium | 2026-03-06 |
| R-12 | document-processing lead | missed source updates, inconsistent hash lineage | weekly | official-source change cannot be traced or replayed | medium | 2026-03-06 |
| R-13 | policy and security lead | restricted redaction analytics exposing practical deanonymization | weekly and before restricted-feature review | one validated deanonymization-like pathway | high | 2026-03-06 |
| R-14 | program manager | unresolved open questions at execution start | weekly | external decisions begin blocking critical-path work | medium | 2026-03-06 |
| R-15 | architecture lead | additional Python packages appear without `uv.lock` updates or the planned package-boundary transition | weekly through early Phase 01 | a second Python package lands without the deliberate manifest split and lock refresh | low | 2026-03-06 |
| R-16 | platform or infrastructure lead | provider-neutral blueprints treated as deploy-ready infra in planning or implementation discussions | weekly through Phase 01 | one attempt to land provider-specific follow-on work without narrowing `OQ-01` or `OQ-02` | medium | 2026-03-06 |
| R-17 | platform or infrastructure lead | local `kind` success cited as proof of higher-environment readiness | weekly through Phase 01 | one higher-environment claim or follow-on decision based only on local `kind` validation | medium | 2026-03-06 |

## R-01: Policy Leakage Through Derived Artifacts

- Status: active
- Source: architecture constraints around victim protection, restricted redaction context, and unsafe-for-LLM spans
- Trigger: summaries, embeddings, search snippets, exports, or QA prompts include restricted context
- Impact: severe legal, ethical, and product integrity failure
- Likelihood: medium
- Mitigation:
  - enforce sensitivity pass before indexing or prompting
  - separate restricted and broad-access indices
  - add policy tests to every retrieval and export path
- Contingency:
  - disable affected endpoint or export immediately
  - invalidate compromised derived assets
  - review audit logs and update policy rules
- Related tasks:
  - P03-T01
  - P03-T02
  - P03-T03
  - P07-T01
  - P07-T02

## R-02: Missing Or Incomplete Provenance

- Status: active
- Source: mandatory provenance architecture invariant
- Trigger: downstream records exist without traceable source tuple or extractor/version metadata
- Impact: loss of evidentiary trust and replayability
- Likelihood: medium
- Mitigation:
  - make provenance fields required in schemas
  - validate at asset boundaries
  - block promotion of invalid artifacts
- Contingency:
  - quarantine invalid assets
  - rerun upstream pipelines from known ingest states
- Related tasks:
  - P00-T02
  - P02-T04
  - P02-T05
  - P05-T06

## R-03: OCR Quality Insufficient For Difficult Material

- Status: active
- Source: corpus difficulty and handwritten/unreliable official search conditions
- Trigger: low OCR confidence, high review load, analyst inability to reconcile page image and extracted text
- Impact: weak evidence usability and downstream extraction errors
- Likelihood: high
- Mitigation:
  - preserve image/native/OCR layers
  - route difficult pages through fallback OCR lanes
  - build gold set for threshold calibration
- Contingency:
  - expand human review queue
  - narrow automation scope on difficult document families
- Related tasks:
  - P02-T03
  - P02-T04
  - P03-T04
  - P05-T06

## R-04: False Positive Identity Merges

- Status: active
- Source: identity resolution complexity
- Trigger: canonical entity combines distinct real-world identities
- Impact: severe analytical distortion across search, graph, timeline, and QA
- Likelihood: medium
- Mitigation:
  - use staged blocking/scoring/clustering
  - require review for high-impact merges
  - keep candidate merges separate from canonical facts
- Contingency:
  - unmerge and rematerialize dependent assets
  - backfill evaluation cases from merge failures
- Related tasks:
  - P04-T01
  - P04-T02
  - P03-T04
  - P05-T02

## R-05: OpenSearch Write Paths Incorrectly Trusted To DLS

- Status: active
- Source: OpenSearch DLS protects reads rather than write APIs
- Trigger: design assumes DLS alone protects ingestion or update paths
- Impact: unauthorized writes or data contamination
- Likelihood: medium
- Mitigation:
  - keep all write paths behind trusted services and service accounts
  - document and test write-path restrictions
- Contingency:
  - rotate credentials
  - reindex from known-good assets
- Related tasks:
  - P03-T03
  - P05-T01
  - P06-T01

## R-06: Graph Semantics Drift Into Co-Mention Noise

- Status: active
- Source: architecture requires event-centric graphing
- Trigger: graph builder emits relationships from raw co-occurrence without evidence class distinctions
- Impact: misleading network exploration and weak QA expansions
- Likelihood: medium
- Mitigation:
  - separate evidence-backed and inferred edges
  - exclude pure co-mention edges by default
  - make edge classes explicit in UI
- Contingency:
  - disable noisy edge classes
  - rebuild graph projections from stricter semantics
- Related tasks:
  - P04-T03
  - P04-T04
  - P05-T02
  - P07-T03

## R-07: QA Ships Before Support Verification Is Credible

- Status: active
- Source: QA abstention and citation requirements
- Trigger: answer generation deployed without robust evidence-pack validation and abstention thresholds
- Impact: hallucinated or overclaimed analyst outputs
- Likelihood: medium
- Mitigation:
  - defer QA behind evidence workbench MVP
  - require support states, citations, and abstention
  - add QA regression suite
- Contingency:
  - restrict QA to internal testing
  - disable answer mode and expose evidence packs only
- Related tasks:
  - P07-T01
  - P07-T02
  - P07-T04

## R-08: Unbounded Scope Creep During Platform Build

- Status: active
- Source: broad architecture and many technology surfaces
- Trigger: new features or integrations are implemented before critical-path evidence capabilities are complete
- Impact: delayed MVP and fragmented system
- Likelihood: high
- Mitigation:
  - enforce dependency map
  - preserve MVP release boundary
  - record new scope in decision log before execution
- Contingency:
  - freeze non-critical streams
  - re-baseline status dashboard and backlog
- Related tasks:
  - all phases

## R-09: State Plane Complexity Causes Operational Instability

- Status: watch
- Source: multiple datastores and orchestration layers
- Trigger: inconsistent config, drift, or poor observability across stateful services
- Impact: deployment failures, degraded lineage, slow recovery
- Likelihood: medium
- Mitigation:
  - GitOps
  - baseline observability
  - environment parity
  - runbook-based operations
- Contingency:
  - degrade to minimum viable services for recovery
  - restore from backups and re-materialize derived assets
- Related tasks:
  - P01-T02
  - P01-T04
  - P01-T06
  - P07-T04

## R-10: Insufficient Gold Data For Threshold Calibration

- Status: active
- Source: OCR, entity resolution, weak supervision, and QA all require evaluation datasets
- Trigger: thresholds set only from intuition or small anecdotal samples
- Impact: unstable quality and untrustworthy release claims
- Likelihood: high
- Mitigation:
  - create gold sets early
  - promote adjudications into eval data
  - track metrics in MLflow
- Contingency:
  - reduce automation scope
  - gate promotion behind larger review samples
- Related tasks:
  - P02-T03
  - P03-T04
  - P05-T05
  - P05-T06
  - P07-T04

## R-11: Frontend Built Against Unstable Or Implicit Contracts

- Status: active
- Source: many dependent services and view models
- Trigger: UI development proceeds without explicit BFF contracts and policy context fields
- Impact: rework, inconsistent semantics, or unsafe client behavior
- Likelihood: medium
- Mitigation:
  - define contracts in Phase 00
  - expose policy_context, provenance_summary, result_confidence consistently
  - favor mock-backed contract development over implicit assumptions
- Contingency:
  - freeze UI work until contracts stabilize
- Related tasks:
  - P00-T04
  - P06-T01
  - P06-T02

## R-12: Ingest Source Updates Are Missed Or Mishandled

- Status: watch
- Source: DOJ corpus may change over time
- Trigger: harvester is not incremental, idempotent, or auditable
- Impact: stale corpus or unverifiable source changes
- Likelihood: medium

## R-16: Provider-Neutral Blueprints Create False Readiness Signals

- Status: watch
- Source: the repository now contains provider-neutral Terraform and Helm baselines before a deployment target and budget envelope are finalized
- Trigger: contributors, PM surfaces, or later tasks treat blueprint-only infra as equivalent to provider-ready provisioning
- Impact: later Phase 01 work could quietly introduce unsafe provider assumptions or claim deployability that does not exist yet
- Likelihood: medium
- Mitigation:
  - keep `OQ-01` and `OQ-02` explicit in the dashboard, backlog, and gap register
  - enforce repository tests that block provider-specific resource types in the current Terraform baseline
  - record a durable decision that the current infra slice is blueprint-only
- Contingency:
  - stop the affected follow-on work
  - re-baseline the PM surfaces to restore the blocked boundary
  - remove any provider-specific drift that landed before the decision boundary was resolved
- Related tasks:
  - `P01-T02`
  - `P01-T03`
  - `P01-T04`
- Mitigation:
  - track source URL, fetch timestamp, headers, hash, and lineage
  - branch each ingest batch in lakeFS
- Contingency:
  - re-harvest from official sources
  - compare hash lineage and reprocess affected branches
- Related tasks:
  - P02-T01
  - P02-T05

## R-15: Python Toolchain Bootstrap Drifts From The Declared Standard

- Status: watch
- Source: the repository now has a normalized root `uv` bootstrap plus multiple shared-library source roots, but future service growth could still reintroduce drift if service packaging expands without an explicit follow-on boundary decision.
- Trigger: a new service or shared library appears without corresponding root validation updates, explicit packaging intent, or `uv.lock` review
- Impact: inconsistent package ownership, dependency drift, and avoidable multi-package bootstrap ambiguity
- Likelihood: low
- Mitigation:
  - keep the current root `uv` bootstrap authoritative until the next explicit packaging transition is executed
  - require `uv sync --dev` and committed `uv.lock` updates for Python dependency changes
  - keep repository-local validation paths aligned to every shared-library source root
  - treat any later service-level package manifest split as explicit follow-on work, not incidental churn
- Contingency:
  - stop adding new Python packages temporarily
  - re-baseline manifests and lockfiles in one bounded migration change
- Related tasks:
  - P01-T01
  - P01-T06

## R-13: Redaction Analytics Become Practically Deanonymizing

- Status: active
- Source: redaction atlas and neighbor-context analysis
- Trigger: combined outputs make protected identity inference materially easier
- Impact: direct violation of architecture and likely unacceptable release risk
- Likelihood: medium
- Mitigation:
  - hash or mask neighborhoods
  - restrict access
  - forbid bulk adjacency export
  - security review restricted features
- Contingency:
  - remove or heavily narrow redaction analytics
- Related tasks:
  - P04-T05
  - P03-T03
  - P07-T03

## R-14: Delivery Stalls On Missing External Decisions

- Status: active
- Source: unresolved deployment, budget, and governance choices
- Trigger: team reaches execution point without explicit decision
- Impact: blocked critical path
- Likelihood: medium
- Mitigation:
  - track open decisions explicitly
  - escalate unresolved items before they become blockers
- Contingency:
  - continue only on research, contracts, or local scaffolding work that does not assume the missing choice
- Related tasks:
  - P00-T01
  - P01-T02
  - P07-T04

## R-17: Local kind Validation Is Mistaken For Higher-Environment Equivalence

- Status: active
- Source: the repository now has an executable internal-only `kind` target that narrows local development but does not replicate higher-environment storage, IAM, DNS, backup, or GPU behavior.
- Trigger: contributors cite local `kind` success as evidence that shared dev, staging, pilot, or production environment decisions are resolved.
- Impact: false confidence, premature task progression, and avoidable rework when higher-environment decisions differ.
- Likelihood: medium
- Mitigation:
  - keep the local-only scope explicit in PM and implementation docs
  - preserve `OQ-01` and `OQ-02` for higher environments
  - avoid higher-environment claims in validation summaries
- Contingency:
  - stop the affected follow-on work
  - re-baseline the backlog and dashboard around the local-only boundary
  - remove any higher-environment assumptions that slipped into code or docs
- Related tasks:
  - P01-T02
  - P01-T03
  - P01-T04

## R-18: Direct Local Control-Plane Bootstrap Is Mistaken For Live Git Reconciliation

- Status: active
- Source: the internal-only `P01-T03` slice now validates Argo CD manifests and the Local secret or certificate path, but part of the live Local validation still installs charts directly before the exact repo state is necessarily present on the tracked remote branch.
- Trigger: contributors cite successful direct Helm or `kubectl` bootstrap as evidence that Argo CD has already reconciled the same repo state from Git.
- Impact: false confidence in GitOps readiness, incomplete `P01-T03` closeout evidence, and later confusion about what was actually exercised.
- Likelihood: medium
- Mitigation:
  - keep the Git remote and tracked-branch boundary explicit in the implementation docs
  - distinguish direct Local bootstrap commands from tracked-remote reconciliation evidence in validation summaries
  - require an explicit follow-on validation or re-baseline before declaring `P01-T03` fully closed
- Contingency:
  - stop any closeout claim that depends on unverified live reconciliation
  - re-baseline the task around the remaining Local follow-on
  - remove or correct any PM text that implies Git reconciliation was already proven when it was not
- Related tasks:
  - P01-T03
  - P01-T04

## Review Rule

Review this register at least once per planning cycle and whenever a task changes from `planned` to `active`.
