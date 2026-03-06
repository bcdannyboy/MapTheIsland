# MapTheIsland PM Workspace

This directory is the persistent program-management surface for building MapTheIsland from the reference architecture in [`Architecture_Plan.md`](../Architecture_Plan.md). It is intended to be read and updated by humans and by future agent sessions. Its purpose is to keep implementation sequencing, policy constraints, research traceability, and execution status stable across long-running development.

## Planning Boundary

This PM workspace does not invent hidden scope. It only plans the platform described in the architecture document:

- a provenance-first evidence platform over the public DOJ corpus
- a victim-protective analytical workflow
- a multilayer system that separates raw evidence, extracted claims, inferred hypotheses, and user interaction
- a policy-bounded evidence workbench with search, graph, analytics, review, and controlled QA

When the architecture leaves a decision unresolved, this workspace records it as an open decision or external prerequisite instead of silently assuming a choice.

## Read Order For New Sessions

1. [`11_status_dashboard.md`](./11_status_dashboard.md)
2. [`01_architecture_constraints.md`](./01_architecture_constraints.md)
3. [`13_glossary.md`](./13_glossary.md)
4. [`14_artifact_inventory.md`](./14_artifact_inventory.md)
5. [`04_dependency_map.md`](./04_dependency_map.md)
6. The active phase backlog file under [`backlog/`](./backlog)
7. [`15_non_functional_requirements.md`](./15_non_functional_requirements.md)
8. [`16_decision_boundaries.md`](./16_decision_boundaries.md)
9. [`17_phase_interlocks.md`](./17_phase_interlocks.md)
10. [`18_environment-and-promotion-model.md`](./18_environment-and-promotion-model.md)
11. [`19_milestone-evidence-packages.md`](./19_milestone-evidence-packages.md)
12. [`20_phase_exit_checklists.md`](./20_phase_exit_checklists.md)
13. [`21_roles_and_responsibilities.md`](./21_roles_and_responsibilities.md)
14. [`22_cross_cutting_requirements.md`](./22_cross_cutting_requirements.md)
15. [`06_risk_register.md`](./06_risk_register.md)
16. [`08_research_register.md`](./08_research_register.md)
17. The latest session log under [`logs/`](./logs)

## File Map

- [`00_program_charter.md`](./00_program_charter.md): project purpose, scope, non-goals, and measurable outcomes.
- [`01_architecture_constraints.md`](./01_architecture_constraints.md): non-negotiable implementation rules translated from the architecture.
- [`02_delivery_operating_model.md`](./02_delivery_operating_model.md): agile execution model, ownership rules, readiness/done criteria, and documentation obligations.
- [`03_phase_plan.md`](./03_phase_plan.md): the master phase sequence and release-oriented framing.
- [`04_dependency_map.md`](./04_dependency_map.md): canonical cross-phase task dependency map and critical path.
- [`05_workstream_index.md`](./05_workstream_index.md): durable workstreams for assigning parallel senior contributors and subagents.
- [`06_risk_register.md`](./06_risk_register.md): active and retired risks with triggers, mitigations, and contingencies.
- [`07_decision_log.md`](./07_decision_log.md): ADR-style implementation decisions.
- [`08_research_register.md`](./08_research_register.md): verified external sources and what planning claims they support.
- [`09_quality_gates.md`](./09_quality_gates.md): mandatory verification gates and blocking release criteria.
- [`10_release_strategy.md`](./10_release_strategy.md): staged release model from internal alpha through production readiness.
- [`11_status_dashboard.md`](./11_status_dashboard.md): current state, active queue, next tasks, blockers, and recent updates.
- [`12_change_log.md`](./12_change_log.md): PM-workspace change history.
- [`13_glossary.md`](./13_glossary.md): canonical program terminology so future sessions do not invent competing definitions.
- [`14_artifact_inventory.md`](./14_artifact_inventory.md): artifact-by-artifact system-of-record, producer, consumer, and promotion rules.
- [`15_non_functional_requirements.md`](./15_non_functional_requirements.md): cross-cutting operational, safety, performance, audit, and recovery requirements.
- [`16_decision_boundaries.md`](./16_decision_boundaries.md): decision classes, signoff expectations, escalation rules, and unresolved-decision handling.
- [`17_phase_interlocks.md`](./17_phase_interlocks.md): phase-to-phase handoff contract, inbound and outbound artifacts, and signoff expectations.
- [`18_environment-and-promotion-model.md`](./18_environment-and-promotion-model.md): environment lifecycle, promotion rules, migration discipline, and rollback expectations.
- [`19_milestone-evidence-packages.md`](./19_milestone-evidence-packages.md): exact evidence required for milestone go or no-go decisions.
- [`20_phase_exit_checklists.md`](./20_phase_exit_checklists.md): concise phase exit evidence checklist for rapid signoff review.
- [`21_roles_and_responsibilities.md`](./21_roles_and_responsibilities.md): owner-role accountability, approval boundaries, and signoff responsibility map.
- [`22_cross_cutting_requirements.md`](./22_cross_cutting_requirements.md): broader cross-phase delivery, lifecycle, security, and governance requirements.
- [`backlog/`](./backlog): detailed phase-by-phase task and subtask plans.
- [`work-packages/`](./work-packages): template for bounded execution packages.
- [`subagents/`](./subagents): operating rules, checklists, and handoff format for future agents.
- [`research/`](./research): source catalog, citation rules, and open research questions.
- [`logs/`](./logs): session-level continuity records.

## Authoritative Sources

If two PM files conflict, authority flows in this order:

1. [`01_architecture_constraints.md`](./01_architecture_constraints.md)
2. [`14_artifact_inventory.md`](./14_artifact_inventory.md)
3. [`16_decision_boundaries.md`](./16_decision_boundaries.md)
4. [`15_non_functional_requirements.md`](./15_non_functional_requirements.md)
5. [`22_cross_cutting_requirements.md`](./22_cross_cutting_requirements.md)
6. [`04_dependency_map.md`](./04_dependency_map.md)
7. relevant phase backlog file
8. [`11_status_dashboard.md`](./11_status_dashboard.md)
9. [`07_decision_log.md`](./07_decision_log.md)

The architecture document remains the primary design source. This PM workspace is the execution layer over that source.

## Task And Dependency Notation

- Phase IDs: `P00` through `P07`
- Task IDs: `PXX-TYY`
- Subtask IDs: `PXX-TYY-SZZ`
- Status values: `planned`, `active`, `blocked`, `done`, `deferred`
- Dependency labels:
  - `blocking`: a hard predecessor must complete first
  - `soft_dependency`: a predecessor improves quality or speed but is not required to start
  - `independent`: no predecessor inside the current plan
  - `parallelizable`: may run alongside named tasks without merge or sequencing conflict

## Update Rules

- Before starting execution, update [`11_status_dashboard.md`](./11_status_dashboard.md) and confirm the target task in the relevant phase backlog.
- When a task changes status, update the phase backlog first, then the dashboard, then the session log.
- When a new risk appears, update [`06_risk_register.md`](./06_risk_register.md) in the same session.
- When a new design choice is made, log it in [`07_decision_log.md`](./07_decision_log.md) before implementation diverges.
- When external research materially affects planning or implementation, append it to [`08_research_register.md`](./08_research_register.md).
- When an artifact class, system of record, or promotion rule changes, update [`14_artifact_inventory.md`](./14_artifact_inventory.md).
- When a cross-cutting quality, safety, performance, or recovery expectation changes, update [`15_non_functional_requirements.md`](./15_non_functional_requirements.md).
- When signoff authority, escalation rules, or blocking decision handling changes, update [`16_decision_boundaries.md`](./16_decision_boundaries.md).
- When environment lifecycle or promotion behavior changes, update [`18_environment-and-promotion-model.md`](./18_environment-and-promotion-model.md).
- When milestone evidence expectations change, update [`19_milestone-evidence-packages.md`](./19_milestone-evidence-packages.md).

## Initial Planning Summary

The current plan uses eight phases:

1. Phase 00: implementation specification and constraints translation
2. Phase 01: platform foundation and control plane
3. Phase 02: immutable ingestion and canonical evidence layer
4. Phase 03: policy enforcement, review loops, and adjudication
5. Phase 04: structured extraction and evidence-backed semantics
6. Phase 05: retrieval, graph, analytics, and hypothesis layer
7. Phase 06: BFF and evidence-workbench UI
8. Phase 07: controlled QA, advanced analytics UI, and production hardening

The first credible release boundary is the evidence workbench, not generalized QA.

## References

- Local architecture basis: [`Architecture_Plan.md`](../Architecture_Plan.md), especially sections 1-4, 17-19, and Part II.
- Verified research catalog: [`08_research_register.md`](./08_research_register.md)
