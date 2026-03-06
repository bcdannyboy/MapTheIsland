# Decision Boundaries

This file makes signoff and escalation rules explicit. The goal is to prevent silent local decisions from altering architecture, policy posture, or release criteria.

## Role Archetypes

These are decision roles, not named people. One person may hold multiple roles, but the decision class still matters.

- Program manager: sequencing, milestone scope, and delivery-state accountability
- Architecture lead: cross-system design integrity, contracts, schema evolution, and critical-path technical tradeoffs
- Platform lead: infra, cluster, secrets, networking, deployment, and stateful-service operations
- Data plane lead: evidence storage, Iceberg, lineage, validation, and large-scale data flows
- Policy and security lead: role model, sensitive handling, exports, audit, and restricted views
- Semantics lead: extraction, resolution, event models, and model-assisted workflows
- Application lead: BFF, UI contracts, route behavior, and analyst ergonomics
- Release lead: quality gates, release packages, rollback readiness, and operational signoff

## Decision Matrix

| Decision Class | Examples | Accountable Role | Must Consult | Required Evidence | Blocking Scope If Unresolved |
| --- | --- | --- | --- | --- | --- |
| architecture invariants | changing truth objects, changing layer separation, changing event-centric graph rule | architecture lead | program manager, policy/security lead | architecture delta and consequence analysis | all affected phases |
| schema or contract breaking change | changing canonical fields, response envelopes, event schemas | architecture lead | data plane lead, application lead, semantics lead | compatibility analysis and migration plan | upstream and downstream tasks touching the contract |
| system-of-record change | moving an artifact to a different store | architecture lead | platform lead, data plane lead, release lead | operational impact and migration path | all producers and consumers of the artifact |
| policy taxonomy change | adding or changing sensitivity classes or export behaviors | policy/security lead | architecture lead, program manager | policy rationale and test impact | indexing, BFF, UI, QA, exports |
| role-definition change | changing who may see or export restricted surfaces | policy/security lead | program manager, application lead, release lead | governance approval path and audit implications | affected routes, stores, and release decisions |
| infrastructure topology change | changing region model, node-pool model, storage strategy | platform lead | architecture lead, data plane lead | capacity and operational impact analysis | platform and all downstream infra-dependent tasks |
| model-provider or model-gateway change | adding or removing providers, changing routing mode | semantics lead | policy/security lead, platform lead | policy impact, cost impact, evaluation impact | model-assisted tasks and QA |
| evaluation-threshold change | changing OCR, retrieval, or QA acceptance thresholds | release lead | semantics lead, data plane lead, program manager | evaluation evidence and rollback implications | release gates and promotion paths |
| milestone scope change | moving features in or out of a release boundary | program manager | architecture lead, release lead, affected workstream leads | dependency and risk impact analysis | current and next milestone |
| release approval | approving alpha, pilot, or production candidate | release lead | program manager, policy/security lead, platform lead, application lead | gate evidence package | release itself |

## Local Decisions That Do Not Require Cross-Program Signoff

The following may be made within a task or work package if they do not violate a higher-level decision:

- internal code organization inside an already approved service boundary
- non-breaking helper-library abstractions
- naming of private functions or modules
- test-fixture structure
- non-breaking UI component decomposition inside an approved route and contract

If a contributor is unsure whether a choice is local or program-level, treat it as program-level until clarified.

## Unresolved-Decision Handling

- If the unresolved item blocks correctness, mark the task blocked.
- If the unresolved item blocks only productionization, work may continue in research or scaffold mode, but the provisional status must be documented.
- If the unresolved item changes release safety, do not continue past prototype or internal-only work.
- If the unresolved item affects policy or legal posture, escalate immediately and do not infer the answer.

## Signoff Evidence Rules

- No signoff is valid without linked artifacts, tests, or validation evidence.
- Phase signoff requires:
  - relevant task completion
  - relevant quality gate evidence
  - updated risk posture
  - updated decision log if any tradeoff was made
- Release signoff requires:
  - quality-gate evidence
  - rollback path
  - operational readiness evidence
  - explicit acknowledgement of open risks

## Default Escalation Triggers

- a contributor needs to change a system of record
- a contributor needs to weaken a policy or quality gate to make progress
- a contract change would cause downstream rework
- a milestone scope change would alter the first credible release boundary
- a numerical threshold is being invented without evaluation evidence

## References

- [`00_program_charter.md`](./00_program_charter.md)
- [`03_phase_plan.md`](./03_phase_plan.md)
- [`04_dependency_map.md`](./04_dependency_map.md)
- [`07_decision_log.md`](./07_decision_log.md)
- [`09_quality_gates.md`](./09_quality_gates.md)
- [`research/open-questions.md`](./research/open-questions.md)
