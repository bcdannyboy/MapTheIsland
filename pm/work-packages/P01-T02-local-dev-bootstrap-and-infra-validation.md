# Work Package

## Header

- Work package ID: `WP-P01-T02-002`
- Date: 2026-03-06
- Related task ID: `P01-T02`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, data and orchestration lead

## Scope

- Objective:
  - Execute the next safe `P01-T02` slice by hardening provider-neutral infra validation, adding executable Helm checks, and narrowing `OQ-01` for internal-only development through a self-managed local cluster target that does not make pilot or production hosting claims.
- In scope:
  - root validation commands for Terraform and Helm
  - CI alignment for the infra validation surface
  - generated-artifact hygiene improvements required by the new validation paths
  - internal-only local-dev cluster configuration and documentation
  - repository tests that lock the new validation surface and local-dev baseline
  - PM and implementation-doc reconciliation for the narrowed local-dev target
- Explicitly out of scope:
  - provider-specific Terraform resources
  - shared dev, staging, pilot, or production hosting decisions
  - live stateful-service deployment beyond cluster-foundation validation
  - secrets, GitOps, certificate, or ingress implementation that depends on `P01-T03`

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `pm/research/open-questions.md`
  - `docs/implementation/platform-foundation-baseline.md`
  - `docs/implementation/engineering-standards-baseline.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `infra/README.md`
  - `infra/terraform/README.md`
  - `infra/helm/README.md`
  - `.github/workflows/ci.yml`
  - `package.json`
- Required upstream tasks:
  - provider-neutral `P01-T02` baseline
  - `P01-T06-S01`
  - `P01-T06-S02`
- Required NFR IDs:
  - `NFR-02`
  - `NFR-06`
  - `NFR-07`
  - `NFR-08`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-010`
  - `D-015`
  - `OQ-01`
  - `OQ-02`

## Dependency Statement

- Hard dependencies confirmed:
  - `P00-T04` complete
  - initial provider-neutral `P01-T02` slice complete
- Soft dependencies acknowledged:
  - `P01-T06-S01/S02` CI baseline complete
  - `P01-T01` shared-library boundary baseline complete
- Parallel workstreams to coordinate with:
  - blocked `P01-T06` observability follow-on only for interface awareness

## Expected Outputs

- Files expected to change:
  - `.github/workflows/ci.yml`
  - `.gitignore`
  - `package.json`
  - `infra/**`
  - `tests/**`
  - relevant PM and implementation docs
- Artifact outputs expected:
  - executable infra validation command surface
  - internal-only local-dev cluster baseline
  - narrowed local interpretation of `OQ-01`
- Tests or validations required:
  - `pnpm check:py`
  - `pnpm check:web`
  - `pnpm check:infra`
  - local cluster bootstrap validation if toolchain is available
- Documentation updates required:
  - Phase 01 backlog
  - status dashboard
  - session log
  - implementation docs for infra validation and local bootstrap guidance
  - research register if external tool docs are used

## Acceptance Criteria

- Criterion 1:
  - Terraform and Helm validation commands exist at the repo root and are enforced locally and in CI.
- Criterion 2:
  - the infra baseline is executable enough to lint and render the platform-foundation chart rather than only asserting file presence.
- Criterion 3:
  - an internal-only local-dev cluster target exists and is documented as a development narrowing of `OQ-01`, not as a pilot or production hosting decision.
- Criterion 4:
  - generated validation artifacts are either ignored or confined so repo hygiene remains stable after local runs.

## Handoff Requirements

- Summary of work completed:
  - record the new validation commands, local-dev cluster baseline, and any narrowed open-question boundaries
- Validation performed:
  - record Python, web, Terraform, Helm, and local cluster commands rerun
- Risks introduced or discovered:
  - record any residual risk that the local-dev target could be mistaken for a broader environment decision
- Follow-up tasks:
  - provider-specific `P01-T02-S02` once hosting and capacity decisions narrow beyond local development
  - `P01-T03`
  - `P01-T04`
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - risk register and decision log if the local-dev target becomes durable
