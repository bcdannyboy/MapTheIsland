# Release Strategy

## Release Philosophy

Release order follows evidence credibility, not UI novelty. Features that make it easier to generate interpretations are released only after the platform can preserve provenance, enforce policy, and expose supporting evidence.

## Milestone R0: Planning Baseline

- Scope:
  - PM workspace
  - implementation spec
  - dependency map
  - research, risk, and decision baselines
- Exit evidence:
  - planning documents complete and internally consistent

## Milestone R1: Evidence Substrate Alpha

- Scope:
  - platform foundation
  - immutable ingest
  - canonical evidence assets
  - baseline validation and lineage
- Required before release:
  - QG-02
  - QG-03
- Intended audience:
  - internal engineering only

## Milestone R2: Policy-Safe Evidence Workbench MVP

- Scope:
  - sensitivity enforcement
  - review/adjudication workflow
  - retrieval indexing
  - BFF
  - search
  - document viewer
  - entity and event views
  - review workbench
- Required before release:
  - QG-04
  - QG-05
  - QG-06
  - QG-07
- Intended audience:
  - internal analyst preview

## Milestone R3: Restricted Analyst Pilot

- Scope:
  - advanced analytics
  - graph explorer
  - topic atlas
  - time-series views
  - tightly controlled redaction analytics
- Required before release:
  - QG-07
  - pilot-specific policy signoff
  - monitoring and rollback plan
- Intended audience:
  - restricted analyst group with approved role set

## Milestone R4: Controlled QA Preview

- Scope:
  - evidence-pack assembly
  - support verification
  - abstention
  - citation UX
- Required before release:
  - QG-08
  - QA regression suite
  - documented role restrictions
- Intended audience:
  - internal reviewers and approved pilot users

## Milestone R5: Production Readiness

- Scope:
  - full release hardening
  - observability and SLO operations
  - recovery and runbooks
  - release governance
- Required before release:
  - QG-09
- Intended audience:
  - approved production operators and analysts

## Rollback Rule

Every release candidate must have:

- a known previous stable milestone
- infra rollback steps
- data rollback or re-materialization strategy
- feature-flag strategy for user-facing surfaces where applicable

## Evidence Package Rule

Every milestone review must point to the exact evidence package defined in [`19_milestone-evidence-packages.md`](./19_milestone-evidence-packages.md). A milestone is not ready for review if its package is incomplete.

## Unresolved-Risk Rule

- A milestone may not pass if unresolved risks exceed the tolerance stated in its evidence package.
- If unresolved risk tolerance is exceeded, either:
  - delay the milestone
  - reduce scope
  - record an explicit exception decision with containment and rollback conditions

## References

- [`03_phase_plan.md`](./03_phase_plan.md)
- [`09_quality_gates.md`](./09_quality_gates.md)
- [`19_milestone-evidence-packages.md`](./19_milestone-evidence-packages.md)
