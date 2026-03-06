# Work Package

## Header

- Work package ID: `WP-P00-T04`
- Date: `2026-03-06`
- Related task ID: `P00-T04`
- Owner: `Architecture Lead`
- Reviewer: `BFF And API Lead`

## Scope

- Objective: convert the architecture's named services and browser boundary into
  a concrete service catalog, API/event inventory, shared-library model, and
  contract versioning policy.
- In scope:
  - service catalog refinement
  - synchronous API inventory
  - asynchronous event inventory
  - contract ownership and versioning rules
- Explicitly out of scope:
  - service runtime implementation
  - infra provisioning
  - BFF route business logic

## Inputs

- Required files:
  - `Architecture_Plan.md`
  - `docs/implementation/implementation-spec-baseline.md`
  - `docs/implementation/architecture-traceability-matrix.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `pm/04_dependency_map.md`
  - `pm/backlog/phase-00-constraints-and-implementation-spec.md`
- Required artifact IDs:
  - `A-028`
  - `A-030`
  - `A-031`
- Required upstream tasks:
  - `P00-T01`
  - `P00-T02`
- Required contracts or schemas:
  - `libs/schemas/src/maptheisland_schemas/evidence.py`
  - `apps/web/README.md`
- Required NFR IDs:
  - `NFR-01`
  - `NFR-10`
  - `NFR-11`
- Required decision IDs or open-question IDs:
  - `D-007`
  - `D-010`
  - `D-011`
- Required research or decisions:
  - `S-016`
  - `S-020`

## Dependency Statement

- Hard dependencies confirmed:
  - `P00-T01` complete
  - `P00-T02` complete
- Soft dependencies acknowledged:
  - `P00-T03` policy definitions will shape export and restricted-route handling
- Parallel workstreams to coordinate with:
  - `P00-T05`
  - `P00-T03`

## Expected Outputs

- Files expected to change:
  - `docs/implementation/implementation-spec-baseline.md`
  - `docs/implementation/architecture-traceability-matrix.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `pm/backlog/phase-00-constraints-and-implementation-spec.md`
  - `pm/11_status_dashboard.md`
  - `pm/07_decision_log.md` if versioning or ownership rules become durable
- Artifact outputs expected:
  - service catalog
  - API inventory
  - async event inventory
  - contract versioning policy
- Handoff target workstream:
  - `architecture`
- Tests or validations required:
  - internal consistency review against the dependency map and browser trust
    boundary constraints
- Documentation updates required:
  - dashboard
  - backlog
  - session log

## Acceptance Criteria

- Criterion 1: every architecture-named service has a scoped responsibility and
  no privileged browser access bypass exists.
- Criterion 2: the core BFF endpoints and cross-service events are named
  explicitly enough for Phase 01 and Phase 06 scaffolding.
- Criterion 3: contract versioning and compatibility rules are written clearly
  enough that future shared-library changes are reviewable.

## Handoff Requirements

- Summary of work completed:
  - note exact files where the service catalog and contract rules live
- Validation performed:
  - dependency and constraint review
- Risks introduced or discovered:
  - especially any contract drift, ownership ambiguity, or policy-boundary gaps
- Follow-up tasks:
  - any API or event contract generation tasks needed in Phase 01
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - decision log if durable contract-governance rules were created
