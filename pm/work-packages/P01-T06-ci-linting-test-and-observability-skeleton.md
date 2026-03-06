# Work Package

## Header

- Work package ID: `WP-P01-T06-001`
- Date: 2026-03-06
- Related task ID: `P01-T06`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, BFF and API lead

## Scope

- Objective:
  - Land the unblocked `P01-T06` slice by creating the initial CI workflow and
    repository build-check automation for Python and web packages, while
    explicitly deferring observability and service-bootstrap documentation that
    depend on later runtime infrastructure.
- In scope:
  - `P01-T06-S01` baseline CI jobs for Python and web validation
  - `P01-T06-S02` workspace build or type-check automation aligned to the
    current repo layout
  - PM and implementation-doc updates needed to record the CI baseline
- Explicitly out of scope:
  - `P01-T06-S03` tracing, metrics, and dashboard collection
  - `P01-T06-S04` final service bootstrap instructions that depend on live
    runtime services
  - provider-specific infrastructure or deployment behavior

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `docs/implementation/engineering-standards-baseline.md`
  - `package.json`
  - `pyproject.toml`
  - `apps/web/package.json`
- Required artifact IDs:
  - none newly introduced
- Required upstream tasks:
  - `P01-T01`
- Required contracts or schemas:
  - current Python and frontend validation baselines
- Required NFR IDs:
  - `NFR-06`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-010`
  - `D-014`
- Required research or decisions:
  - none

## Dependency Statement

- Hard dependencies confirmed:
  - `P01-T01` complete
- Soft dependencies acknowledged:
  - none
- Parallel workstreams to coordinate with:
  - provider-neutral `P01-T02` planning only

## Expected Outputs

- Files expected to change:
  - CI workflow files under `.github/workflows/`
  - root and workspace manifests or config files only if validation wiring needs adjustment
  - relevant PM and implementation docs
- Artifact outputs expected:
  - baseline repository CI workflow
  - explicit repository build-check path for Python and web validation
- Handoff target workstream:
  - `WS-01 Platform And Infrastructure`
- Tests or validations required:
  - local Python validation baseline
  - local frontend validation baseline
  - syntax validation for workflow files if a local tool is available
- Documentation updates required:
  - backlog
  - dashboard
  - session log
  - engineering baseline if commands or CI expectations change

## Acceptance Criteria

- Criterion 1:
  - Python and web validation paths can run automatically in CI from the
    current monorepo layout.
- Criterion 2:
  - the CI slice respects the 100 percent pass and 100 percent coverage rule
    already encoded in repository commands.
- Criterion 3:
  - blocked observability work remains explicitly deferred rather than implied.

## Handoff Requirements

- Summary of work completed:
  - record the CI jobs or workflow files added
- Validation performed:
  - record the local commands rerun after the workflow lands
- Risks introduced or discovered:
  - record any CI-environment, cache, or tooling-version risk
- Follow-up tasks:
  - remaining `P01-T06-S03`
  - remaining `P01-T06-S04`
- Required PM updates:
  - backlog
  - dashboard
  - session log

## Current Status

- Status:
  - partially complete and currently blocked
- Summary of work completed:
  - added `.github/workflows/ci.yml` for root Python and web validation
  - added root `check:web` automation
  - added a regression test for the CI workflow baseline
- Validation performed:
  - `pnpm check:py`
  - `pnpm check:web`
- Risks introduced or discovered:
  - none beyond existing tooling-version and later observability dependencies
- Follow-up tasks:
  - complete `P01-T06-S03` once `P01-T04-S04` lands
  - complete `P01-T06-S04` after observability and runtime bootstrap surfaces
    exist
