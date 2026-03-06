# Work Package

## Header

- Work package ID: `WP-P01-T03-001`
- Date: 2026-03-06
- Related task ID: `P01-T03`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, policy and security lead

## Scope

- Objective:
  - Execute the first safe internal-only `P01-T03` slice by publishing the
    local control-plane baseline for GitOps, secret delivery, and certificate
    ownership on top of the validated `kind` target without making
    higher-environment readiness claims.
- In scope:
  - internal-only `P01-T03` work-package activation and PM reconciliation
  - Argo CD bootstrap and application-manifest baseline for Local
  - local-only Vault plus External Secrets integration path
  - local-only cert-manager plus self-signed issuer baseline
  - a sample secret and certificate consumer manifest set in the application
    namespace
  - root repository commands for cluster-free control-plane validation and
    local integration checks
  - repository tests and CI updates that lock the new control-plane surfaces
  - implementation documentation that resolves the local portion of `GAP-012`
- Explicitly out of scope:
  - higher-environment GitOps rollout
  - higher-environment Vault auth backend choice
  - external CA, ACME, DNS, or ingress integration
  - pilot or production certificate trust claims
  - stateful service rollout from `P01-T04`

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `pm/research/open-questions.md`
  - `pm/06_risk_register.md`
  - `pm/07_decision_log.md`
  - `docs/implementation/local-dev-platform-target.md`
  - `docs/implementation/platform-foundation-baseline.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `infra/README.md`
  - `infra/helm/README.md`
  - `infra/kind/README.md`
  - `.github/workflows/ci.yml`
  - `package.json`
- Required upstream tasks:
  - internal-only `P01-T02` local-dev target baseline
  - `P01-T01`
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
  - `D-016`
  - `OQ-01`
  - `OQ-02`
  - `GAP-012`
- Required research or decisions:
  - current official Argo CD installation and cluster-bootstrapping guidance
  - current official External Secrets and Vault provider guidance
  - current official cert-manager Helm and self-signed issuer guidance

## Dependency Statement

- Hard dependencies confirmed:
  - internal-only `P01-T02` local-dev target complete
  - provider-neutral `P01-T02` baseline complete
- Soft dependencies acknowledged:
  - `P01-T06-S01/S02` CI baseline complete
  - higher-environment `OQ-01` and `OQ-02` remain open
- Parallel workstreams to coordinate with:
  - blocked `P01-T06` observability follow-on for interface awareness only
  - local-only preparatory `P01-T04` planning after this slice lands

## Expected Outputs

- Files expected to change:
  - `package.json`
  - `.github/workflows/ci.yml`
  - `.gitignore`
  - `infra/**`
  - `docs/implementation/**`
  - `tests/**`
  - relevant PM docs
- Artifact outputs expected:
  - repo-managed local control-plane baseline
  - local-only secret bootstrap and tenancy model
  - local-only certificate ownership model
  - repeatable cluster-free and cluster-backed validation commands
- Handoff target workstream:
  - `P01-T04` local-only preparatory work
- Tests or validations required:
  - `pnpm check:py`
  - `pnpm check:web`
  - `pnpm check:infra`
  - `pnpm check:control-plane`
  - local `kind` integration validation for the new control-plane commands if
    the toolchain remains available
- Documentation updates required:
  - Phase 01 backlog
  - status dashboard
  - session log
  - implementation docs for the local control-plane baseline
  - research register
  - decision log
  - risk register

## Acceptance Criteria

- Criterion 1:
  - The repository publishes an internal-only local GitOps baseline centered on
    Argo CD manifests, a root bootstrap application, and a documented repo URL
    boundary that does not pretend higher-environment readiness.
- Criterion 2:
  - The repository publishes a local-only Vault plus External Secrets path that
    keeps bootstrap token material out of Git and materializes runtime secrets
    only into consuming namespaces.
- Criterion 3:
  - The repository publishes a local-only cert-manager baseline with explicit
    ownership of issued certificate secrets and a sample application manifest
    path that depends on those certificates.
- Criterion 4:
  - The new control-plane surfaces are locked by repository tests and by
    cluster-free validation commands, with live local integration validation
    recorded separately when the local toolchain is available.

## Handoff Requirements

- Summary of work completed:
  - record the local-only GitOps, secret-delivery, and certificate baselines
- Validation performed:
  - record cluster-free control-plane validation plus any live `kind`
    integration checks
- Risks introduced or discovered:
  - record any residual risk that direct local validation is confused with live
    Git reconciliation or higher-environment readiness
- Follow-up tasks:
  - complete or re-baseline the remaining `P01-T03` subtasks based on what is
    validated live
  - advance local-only `P01-T04` once the control-plane path is stable
  - keep higher-environment follow-on blocked until `OQ-01` and `OQ-02`
    narrow further
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - decision log
  - risk register
  - research register
  - implementation-gap register
