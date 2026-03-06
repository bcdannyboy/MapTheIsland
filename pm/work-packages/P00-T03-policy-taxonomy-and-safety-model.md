# Work Package

## Header

- Work package ID: `WP-P00-T03`
- Date: `2026-03-06`
- Related task ID: `P00-T03`
- Owner: `Policy And Security Lead`
- Reviewer: `Architecture Lead`

## Scope

- Objective: define the explicit policy baseline that governs sensitivity,
  restricted context, prohibited flows, role intent, and policy validation
  expectations before later semantic and QA work proceeds.
- In scope:
  - sensitivity taxonomy
  - role and export-intent matrix
  - prohibited-flow catalog
  - initial policy test matrix
- Explicitly out of scope:
  - live policy-engine implementation
  - production role provisioning
  - datastore enforcement code

## Inputs

- Required files:
  - `Architecture_Plan.md`
  - `pm/01_architecture_constraints.md`
  - `pm/11_status_dashboard.md`
  - `pm/backlog/phase-00-constraints-and-implementation-spec.md`
  - `docs/implementation/implementation-spec-baseline.md`
  - `docs/implementation/open-implementation-gaps.md`
- Required artifact IDs:
  - `A-011`
  - `A-012`
- Required upstream tasks:
  - `P00-T01`
  - `P00-T02`
- Required contracts or schemas:
  - `libs/schemas/src/maptheisland_schemas/evidence.py`
- Required NFR IDs:
  - `NFR-03`
  - `NFR-05`
  - `NFR-10`
  - `NFR-11`
- Required decision IDs or open-question IDs:
  - `D-004`
  - `D-010`
  - `OQ-03`
- Required research or decisions:
  - `S-001`
  - `S-002`
  - `S-013`

## Dependency Statement

- Hard dependencies confirmed:
  - `P00-T01` complete
- Soft dependencies acknowledged:
  - `P00-T04` service-boundary work should stay coordinated because role and
    export decisions affect BFF and review APIs
- Parallel workstreams to coordinate with:
  - `P00-T04`
  - `P00-T05`

## Expected Outputs

- Files expected to change:
  - `docs/implementation/implementation-spec-baseline.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `pm/backlog/phase-00-constraints-and-implementation-spec.md`
  - `pm/11_status_dashboard.md`
  - `pm/07_decision_log.md` if durable choices are made
- Artifact outputs expected:
  - sensitivity taxonomy baseline
  - role/export matrix baseline
  - prohibited-flow catalog
  - policy-verification matrix
- Handoff target workstream:
  - `policy/security`
- Tests or validations required:
  - document-level consistency review against `AC-02`, `AC-08`, `AC-10`,
    `AC-12`, and `AC-15`
- Documentation updates required:
  - dashboard
  - phase backlog
  - session log
  - risk register if new policy or governance risks appear

## Acceptance Criteria

- Criterion 1: every sensitivity class and restricted-context case named by the
  architecture is represented explicitly.
- Criterion 2: prohibited flows around redactions, QA prompting, and export are
  unambiguous and non-contradictory.
- Criterion 3: the resulting policy matrix is usable as an implementation and
  test authoring baseline for Phase 03.

## Handoff Requirements

- Summary of work completed:
  - which files define the taxonomy, matrices, and flow catalog
- Validation performed:
  - architecture and constraint cross-check
- Risks introduced or discovered:
  - especially any unresolved governance dependencies tied to `OQ-03`
- Follow-up tasks:
  - any new backlog entries needed for enforcement or testing
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - decision log if a durable policy choice was made
