# Non-Functional Requirements

This document centralizes cross-cutting requirements that are implied by the architecture but should not remain scattered across multiple files. These requirements apply to implementation, testing, release decisions, and operational acceptance.

## NFR-01 Provenance Completeness

- Meaning: every analyst-visible or downstream-consumable artifact must preserve traceability to source evidence and processing lineage.
- Applies to: all phases, all services, all stores
- Minimum evidence of compliance:
  - required provenance fields exist
  - traceability can be traversed from UI output back to source evidence

## NFR-02 Deterministic Replayability

- Meaning: ingest and downstream asset generation must be replayable from a known raw-evidence state and versioned processing surface.
- Applies to: ingest, docproc, extraction, indexing, graph, QA evidence-pack assembly
- Minimum evidence of compliance:
  - branch-scoped ingest state exists
  - failed branches remain auditable
  - rematerialization procedures are documented and tested

## NFR-03 Policy Safety

- Meaning: restricted or unsafe context may not leak through indices, prompts, exports, caches, logs, or UI rendering.
- Applies to: indexing, BFF, UI, QA, exports, logs, analytics
- Minimum evidence of compliance:
  - policy tests exist
  - deny paths are validated
  - restricted rendering is demonstrably gated

## NFR-04 Evidentiary Honesty

- Meaning: the product may not imply a stronger degree of certainty than the source or pipeline justifies.
- Applies to: document viewer, thread reconstruction, temporal normalization, graph views, QA
- Minimum evidence of compliance:
  - confidence and uncertainty are visible where required
  - image/native/OCR distinctions are exposed
  - inferred relationships are visually distinct from evidence-backed ones

## NFR-05 Auditability

- Meaning: sensitive reads, review actions, adjudications, exports, and policy denies must be reconstructable after the fact.
- Applies to: review, export, QA, admin, policy enforcement
- Minimum evidence of compliance:
  - audit events are written
  - correlation from action to actor and artifact exists
  - audit records are retained according to the chosen governance policy

## NFR-06 Observability

- Meaning: the system must expose enough traces, metrics, logs, and dashboards for operators to understand ingest health, search health, review load, and QA behavior.
- Applies to: platform, data plane, review, search, QA
- Minimum evidence of compliance:
  - baseline dashboards exist
  - alerts exist for critical failure classes
  - latency and queue-depth metrics are available

## NFR-07 Recoverability

- Meaning: the platform must be able to recover from service failure, data corruption, release rollback, or bad derived-asset promotion without unrecoverable state loss.
- Applies to: all stateful systems and release processes
- Minimum evidence of compliance:
  - backup and restore path exists
  - rollback or rematerialization path exists
  - recovery drills are documented and executed before production readiness

## NFR-08 Performance And Capacity Transparency

- Meaning: performance must be measurable even where hard numeric budgets are not yet finalized.
- Applies to: BFF, search, document viewer, review workbench, QA, analytics
- Minimum evidence of compliance:
  - request timings and queue metrics are captured
  - benchmark harnesses exist for critical paths
  - unresolved numeric SLOs are tracked as explicit implementation-spec decisions

Hard numerical budgets are intentionally not invented here. They must be set in the implementation spec when deployment environment, budget, and audience are known.

## NFR-09 Scalability Of Artifact Growth

- Meaning: storage and indexing strategy must tolerate the expected growth of raw evidence, derived assets, and review data without ad hoc redesign.
- Applies to: object storage, Iceberg, PostgreSQL, OpenSearch, Neo4j
- Minimum evidence of compliance:
  - partitioning and retention strategies are defined
  - growth monitoring exists
  - large-fanout jobs are routed to the intended compute layer

## NFR-10 Security Of Trust Boundaries

- Meaning: human users, service accounts, model gateways, datastores, and exports must have distinct trust boundaries.
- Applies to: auth, policy, network, secrets, model access, UI
- Minimum evidence of compliance:
  - browser never receives privileged datastore credentials
  - service-only write paths are enforced where required
  - short-lived scoped URLs are used for sensitive object access

## NFR-11 Testability And Evaluation Coverage

- Meaning: major workflows must be testable with repeatable suites, and model-assisted behaviors must be measurable against evaluation datasets.
- Applies to: all phases, with special emphasis on OCR, extraction, retrieval, QA, and release engineering
- Minimum evidence of compliance:
  - local automated test suites exist and pass at 100 percent
  - integration test suites exist and pass at 100 percent
  - handwritten code is maintained at 100 percent coverage
  - unit, integration, and end-to-end strategy exists
  - evaluation datasets are versioned
  - regression thresholds are explicit
- Enforcement note:
  - no task, phase, or release is complete while any relevant test is failing or any handwritten code path is uncovered

## NFR-12 Accessibility And Analyst Ergonomics

- Meaning: the analyst workbench must be usable for long-lived review and inspection sessions.
- Applies to: web shell, document viewer, review workbench, analytics views
- Minimum evidence of compliance:
  - keyboard-heavy review flows are supported
  - critical evidence views remain legible and navigable
  - uncertainty and policy state are visible instead of buried

## NFR-13 Documentation Continuity

- Meaning: planning, risk, research, decision, and session state must remain usable across long-running multi-agent development.
- Applies to: `/pm` and all future delivery work
- Minimum evidence of compliance:
  - dashboard is current
  - relevant backlog file is current
  - decisions and new external research are logged

## References

- [`Architecture_Plan.md`](../Architecture_Plan.md): lines 1-20, 24-26, 64-74, 89-109, 127-129, 167-171, 211-223, 247-259, 295-297, 367-377, 413-462
- [`08_research_register.md`](./08_research_register.md)
- [`09_quality_gates.md`](./09_quality_gates.md)
