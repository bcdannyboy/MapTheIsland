# Work Package

## Header

- Work package ID: `WP-P01-T03-002`
- Date: 2026-03-06
- Related task ID: `P01-T03`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, policy and security lead

## Scope

- Objective:
  - Close the remaining Local `P01-T03` boundary by validating that Argo CD
    can reconcile the repo-managed Local control-plane manifests from the
    tracked public Git remote on `main`, not just from direct Local bootstrap
    commands.
- In scope:
  - repository reconciliation for the remaining Local GitOps follow-on
  - explicit tracked-remote command publication for Local bootstrap and status
    checks
  - repo test updates that lock the new command surface and boundary language
  - moving the tracked public Git remote into alignment with the current repo
    state when safe
  - live Local validation that distinguishes:
    - direct Argo CD installation
    - repo-managed bootstrap manifest apply
    - live tracked-remote reconciliation of child applications
  - PM and implementation-doc reconciliation after the result is known
- Explicitly out of scope:
  - higher-environment GitOps rollout
  - higher-environment Vault auth backend choice
  - higher-environment certificate authority or ingress integration
  - any provider-specific `P01-T02` follow-on
  - stateful service rollout from `P01-T04`

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `pm/06_risk_register.md`
  - `pm/07_decision_log.md`
  - `pm/18_environment-and-promotion-model.md`
  - `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`
  - `docs/implementation/local-dev-platform-target.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `infra/gitops/README.md`
  - `package.json`
  - `tests/test_gitops_control_plane_baseline.py`
  - `tests/test_workspace_baseline.py`
- Required upstream tasks:
  - Local `P01-T02` baseline complete
  - Local `P01-T03` first slice complete
- Required NFR IDs:
  - `NFR-02`
  - `NFR-06`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-010`
  - `D-016`
  - `D-017`
  - `D-018`
  - `R-18`

## Dependency Statement

- Hard dependencies confirmed:
  - Local `kind` target is validated
  - Local control-plane manifests exist
  - public Git remote and branch are fixed in the manifests
- Blocking condition to resolve:
  - the tracked remote must actually contain the repo state being validated, or
    the task must be re-baselined explicitly
- Parallel workstreams to coordinate with:
  - local-only `P01-T04` preparation may begin only after this boundary is
    closed or formally re-baselined

## Expected Outputs

- Files expected to change:
  - `package.json`
  - `README.md`
  - `infra/gitops/README.md`
  - `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`
  - `docs/implementation/local-dev-platform-target.md`
  - `tests/test_gitops_control_plane_baseline.py`
  - `tests/test_workspace_baseline.py`
  - relevant PM docs
- Artifact outputs expected:
  - explicit tracked-remote Local GitOps bootstrap command
  - explicit tracked-remote Local GitOps reconciliation check command
  - validation evidence that either proves or cleanly re-baselines live
    tracked-remote reconciliation
- Tests or validations required:
  - `pnpm check:py`
  - `pnpm check:web`
  - `pnpm check:infra`
  - `pnpm check:control-plane`
  - `pnpm create:kind:dev`
  - `pnpm apply:kind:argocd`
  - `pnpm apply:kind:argocd:gitops`
  - `pnpm check:kind:argocd:remote-reconciliation`
  - `pnpm delete:kind:dev`

## Acceptance Criteria

- Criterion 1:
  - The repository publishes a distinct command surface for tracked-remote
    Local GitOps bootstrap and reconciliation checks.
- Criterion 2:
  - The tracked remote either contains the validated repo state or the task is
    explicitly re-baselined instead of overstated.
- Criterion 3:
  - Validation evidence distinguishes direct Local bootstrap from live
    tracked-remote reconciliation.
- Criterion 4:
  - PM, implementation docs, and tests all reflect the resolved boundary.

## Handoff Requirements

- Summary of work completed:
  - record whether live tracked-remote reconciliation was validated or
    re-baselined
- Validation performed:
  - record exact Local commands and the resulting Argo CD sync or health
    evidence
- Risks introduced or discovered:
  - update the risk register if the tracked-remote path remains misleading or
    operationally brittle
- Follow-up tasks:
  - move to local-only `P01-T04` once this boundary is resolved
  - keep higher-environment follow-on blocked until `OQ-01` and `OQ-02` narrow
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - decision log if a durable path choice is made
  - risk register
  - implementation docs
