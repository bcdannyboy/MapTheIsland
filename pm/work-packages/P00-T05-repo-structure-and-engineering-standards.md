# Work Package

## Header

- Work package ID: `WP-P00-T05`
- Date: `2026-03-06`
- Related task ID: `P00-T05`
- Owner: `Evaluation And Release Lead`
- Reviewer: `Architecture Lead`

## Scope

- Objective: finish the engineering baseline so the repo structure, toolchain,
  testing gates, and contributor expectations are stable before multi-service
  implementation accelerates.
- In scope:
  - monorepo folder standard
  - Python and frontend workspace rules
  - CI and review conventions
  - contribution expectations tied to quality gates
- Explicitly out of scope:
  - full CI pipeline implementation
  - service-specific runtime code
  - production deployment automation

## Inputs

- Required files:
  - `docs/implementation/implementation-spec-baseline.md`
  - `package.json`
  - `pnpm-workspace.yaml`
  - `pyproject.toml`
  - `apps/web/README.md`
  - `pm/09_quality_gates.md`
  - `pm/20_phase_exit_checklists.md`
  - `pm/backlog/phase-00-constraints-and-implementation-spec.md`
- Required artifact IDs:
  - `A-010`
- Required upstream tasks:
  - `P00-T01`
- Required contracts or schemas:
  - current shared schema baseline in `libs/schemas`
- Required NFR IDs:
  - `NFR-06`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-010`
  - `D-011`
- Required research or decisions:
  - `S-005`
  - `S-019`

## Dependency Statement

- Hard dependencies confirmed:
  - `P00-T01` complete
- Soft dependencies acknowledged:
  - `P00-T04` contract versioning will influence final frontend standards
- Parallel workstreams to coordinate with:
  - `P00-T04`
  - `P00-T03`

## Expected Outputs

- Files expected to change:
  - `pyproject.toml`
  - `package.json`
  - `pnpm-workspace.yaml`
  - `apps/web/README.md`
  - `pm/backlog/phase-00-constraints-and-implementation-spec.md`
  - `pm/11_status_dashboard.md`
  - `pm/06_risk_register.md` if toolchain drift remains material
- Artifact outputs expected:
  - finalized repo structure standard
  - Python engineering standard
  - frontend engineering standard
  - CI and review standard
- Handoff target workstream:
  - `validation/release`
- Tests or validations required:
  - local lint, typing, and test checks
  - manifest validation for workspace files
- Documentation updates required:
  - dashboard
  - backlog
  - session log
  - change log if new root standards are introduced

## Acceptance Criteria

- Criterion 1: the repository layout is explicit and aligned to the architecture.
- Criterion 2: Python and frontend tooling expectations are documented without
  ambiguity, including the path to a normalized `uv` bootstrap.
- Criterion 3: CI and review rules encode the non-negotiable 100 percent pass
  and coverage requirements.

## Handoff Requirements

- Summary of work completed:
  - identify the repo-standard and tooling files created or updated
- Validation performed:
  - list lint, test, typecheck, and manifest checks run
- Risks introduced or discovered:
  - especially toolchain drift or unresolved install/bootstrap gaps
- Follow-up tasks:
  - CI implementation or dependency-bootstrap work still needed
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - risk register if the toolchain gap remains active
