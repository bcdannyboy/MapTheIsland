# Work Package

## Header

- Work package ID: `WP-P01-T04-001`
- Date: 2026-03-06
- Related task ID: `P01-T04`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, data plane lead

## Scope

- Objective:
  - Start the local-only `P01-T04` lane by standing up the first persistent
    state-plane services required for ingest replay and operational metadata:
    S3-compatible object storage plus lakeFS, and PostgreSQL with schema
    management wired into the Local control-plane baseline.
- In scope:
  - local-only object-storage baseline
  - local-only lakeFS baseline
  - local-only PostgreSQL baseline
  - initial credential and namespace wiring through the existing Local
    control-plane path
  - bounded validation commands and repository tests for the new Local
    state-plane surfaces
  - implementation and PM updates that make the Local-only boundary explicit
- Explicitly out of scope:
  - Kafka, OpenSearch, Neo4j, and Trino
  - higher-environment storage or database rollout
  - production-authoritative backup, throughput, or HA claims
  - ingest-service runtime implementation from Phase 02

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `pm/06_risk_register.md`
  - `pm/07_decision_log.md`
  - `docs/implementation/service-boundaries-and-contracts.md`
  - `docs/implementation/platform-foundation-baseline.md`
  - `docs/implementation/local-dev-platform-target.md`
  - `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `infra/gitops/README.md`
  - `package.json`
- Required upstream tasks:
  - `P01-T02`
  - `P01-T03`
  - `P00-T02`
- Required NFR IDs:
  - `NFR-02`
  - `NFR-06`
  - `NFR-07`
  - `NFR-08`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-003`
  - `D-015`
  - `D-016`
  - `D-018`
  - `D-019`
  - `OQ-01`
  - `OQ-02`

## Dependency Statement

- Hard dependencies confirmed:
  - the Local `kind` target is validated
  - Local tracked-remote Git reconciliation is validated
  - Local control-plane secret delivery is available
  - the shared evidence schema baseline exists
- Soft dependencies acknowledged:
  - higher-environment rollout remains blocked on `OQ-01` and `OQ-02`
  - future Kafka and catalog work will depend on the service choices made here
- Parallel workstreams to coordinate with:
  - later `P01-T04-S03` state-plane expansion
  - blocked `P01-T06-S03/S04` observability follow-on after `P01-T04-S04`

## Expected Outputs

- Files expected to change:
  - `package.json`
  - `infra/gitops/`
  - `infra/helm/values/`
  - `services/README.md`
  - `docs/implementation/`
  - `tests/`
  - relevant PM docs
- Artifact outputs expected:
  - Local object-storage and lakeFS baseline
  - Local PostgreSQL baseline with schema-management entry point
  - bounded validation commands for Local state-plane bootstrap and health
  - repository tests that lock the new Local state-plane contract
- Handoff target workstream:
  - `WS-02 Data Plane And Orchestration`
- Tests or validations required:
  - `pnpm check:py`
  - `pnpm check:web`
  - `pnpm check:infra`
  - `pnpm check:control-plane`
  - new Local state-plane validation commands added by this slice
- Documentation updates required:
  - implementation baseline for the Local state plane
  - PM backlog, dashboard, risk, change-log, and session-log updates

## Acceptance Criteria

- Criterion 1:
  - Local object storage plus lakeFS are deployable, health-checkable, and
    scoped explicitly to Local-only development.
- Criterion 2:
  - Local PostgreSQL is deployable, health-checkable, and prepared for
    schema-management flow without weakening the Local-only boundary.
- Criterion 3:
  - credentials, connectivity checks, and repository tests make the new
    Local state-plane surfaces reproducible and auditable.

## Handoff Requirements

- Summary of work completed:
  - record which `P01-T04-S01` and `P01-T04-S02` surfaces landed in the first
    Local slice
- Validation performed:
  - record exact Local bootstrap and health-check commands
- Risks introduced or discovered:
  - update the risk register for Local resource pressure, false readiness, or
    cleanup or retention concerns
- Follow-up tasks:
  - continue into the remaining `P01-T04` subtasks once this Local state-plane
    slice is stable
  - keep higher-environment follow-on blocked until `OQ-01` and `OQ-02` narrow
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - decision log if a durable state-plane choice is made
  - risk register
  - implementation docs
