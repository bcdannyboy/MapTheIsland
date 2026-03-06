# Work Package

## Header

- Work package ID: `WP-P01-T01-001`
- Date: 2026-03-06
- Related task ID: `P01-T01`
- Owner: architecture lead
- Reviewer: BFF and API lead, platform or infrastructure lead

## Scope

- Objective:
  - Execute the first bounded `P01-T01` slice by turning the Phase 00
    `libs/contracts` and `libs/policy` placeholders into executable shared
    library scaffolds, updating the Python workspace and validation surfaces so
    the new package boundaries are explicit and testable, and documenting the
    ownership and contribution path for shared libraries and reserved services.
- In scope:
  - executable Python source roots for `libs/contracts` and `libs/policy`
  - minimal contract models aligned to the published Phase 00 event and policy
    baselines
  - repository test and type-check configuration updates needed to keep the new
    handwritten code at 100 percent coverage
  - explicit ownership and contribution guidance for `libs/` and `services/`
  - PM and implementation-doc reconciliation for the Phase 01 kickoff
- Explicitly out of scope:
  - provider-specific infrastructure choices
  - live Kubernetes, Terraform, Helm, Argo CD, Vault, or cert-manager
    implementation
  - runtime service logic for `bff`, `review-api`, or other reserved services
  - final role-governance decisions blocked by `OQ-03`
  - broker-level topic names, retention policy, or model-provider assumptions

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `pm/21_roles_and_responsibilities.md`
  - `docs/implementation/service-boundaries-and-contracts.md`
  - `docs/implementation/policy-taxonomy-and-safety-model.md`
  - `docs/implementation/engineering-standards-baseline.md`
  - `pyproject.toml`
  - `tests/conftest.py`
- Required artifact IDs:
  - `A-032`
  - `A-033`
  - `A-034`
- Required upstream tasks:
  - `P00-T04`
  - `P00-T05`
- Required contracts or schemas:
  - published async event envelope minimum
  - shared-library ownership model
  - deny-by-default policy baseline
- Required NFR IDs:
  - `NFR-10`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-012`
  - `D-013`
  - `OQ-03`
- Required research or decisions:
  - none beyond the accepted Phase 00 baseline

## Dependency Statement

- Hard dependencies confirmed:
  - `P00-T04` complete
  - `P00-T05` complete
- Soft dependencies acknowledged:
  - `P01-T06` will consume the workspace and validation updates from this slice
- Parallel workstreams to coordinate with:
  - future `P01-T06` CI baseline
  - provider-neutral `P01-T02` planning only

## Expected Outputs

- Files expected to change:
  - `pyproject.toml`
  - `tests/conftest.py`
  - `libs/contracts/**`
  - `libs/policy/**`
  - `libs/README.md`
  - `services/README.md`
  - relevant PM and implementation docs
- Artifact outputs expected:
  - executable baseline for `A-033` async event contract package
  - executable baseline for `A-034` policy taxonomy and capability matrix
  - documented ownership or contribution map for shared libraries and services
- Handoff target workstream:
  - `WS-01 Platform And Infrastructure`
  - `WS-02 Data Plane And Orchestration`
- Tests or validations required:
  - `UV_CACHE_DIR=.uv-cache uv run ruff check .`
  - `UV_CACHE_DIR=.uv-cache uv run mypy libs/schemas/src libs/contracts/src libs/policy/src tests`
  - `UV_CACHE_DIR=.uv-cache uv run pytest`
- Documentation updates required:
  - relevant Phase 01 backlog state
  - status dashboard
  - session log
  - implementation docs if contract or workspace rules become more explicit

## Acceptance Criteria

- Criterion 1:
  - `libs/contracts` and `libs/policy` are executable shared-library scaffolds
    rather than placeholder-only directories.
- Criterion 2:
  - repository validation and coverage configuration include the new handwritten
    code and still enforce 100 percent coverage and 100 percent pass rates.
- Criterion 3:
  - ownership and contribution boundaries for shared libraries and reserved
    services are explicit enough that later service work can start without
    structural churn.

## Handoff Requirements

- Summary of work completed:
  - describe the package-boundary and tooling changes made in this slice
- Validation performed:
  - record Ruff, mypy, pytest, and any relevant frontend validation outputs
- Risks introduced or discovered:
  - record any package-management, import-path, or ownership ambiguity risks
- Follow-up tasks:
  - `P01-T06`
  - remaining `P01-T01` service-scaffold and ownership refinements if any
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - risk register or decision log if the package-boundary transition changes
    durable repository rules

## Current Status

- Status:
  - complete
- Summary of work completed:
  - added executable `libs/contracts` and `libs/policy` shared-library source
    roots
  - expanded root Python validation to cover `libs/schemas/src`,
    `libs/contracts/src`, `libs/policy/src`, and `tests`
  - documented ownership and contribution paths across `libs/` and `services/`
  - updated implementation, decision, artifact, risk, and session-tracking
    surfaces for the deliberate shared-library package-boundary transition
- Validation performed:
  - `pnpm check:py`
  - `pnpm check:web`
- Risks introduced or discovered:
  - future service-level package manifests still require an explicit bounded
    transition and remain tracked in `R-15`
- Follow-up tasks:
  - `P01-T06`
  - provider-neutral `P01-T02`
