# Work Package

## Header

- Work package ID: `WP-P01-T02-002`
- Date: 2026-03-06
- Related task ID: `P01-T02`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, data and orchestration lead

## Scope

- Objective:
  - Narrow `OQ-01` and the safe local portion of `OQ-02` by defining an internal-only self-managed local development target that can validate the MapTheIsland cluster baseline without making a staging, pilot, or production provider commitment.
- In scope:
  - local self-managed Kubernetes target for internal development only
  - executable local cluster configuration and validation surface
  - simulated node-pool role mapping for `general`, `stateful`, and `gpu`
  - Helm foundation values and rendering path for the local target
  - local infra validation commands and repository tests for the new local target surfaces
  - PM and implementation-doc updates required to narrow `OQ-01` and `OQ-02` safely
- Explicitly out of scope:
  - cloud or on-prem provider selection for higher environments
  - live stateful-service deployment beyond cluster-baseline validation
  - Argo CD, Vault, External Secrets Operator, or cert-manager implementation
  - production-authoritative sizing, GPU guarantees, or backup claims
  - any claim that the local target satisfies staging, pilot, or production readiness

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
- Required upstream tasks:
  - `P00-T04`
  - provider-neutral `P01-T02-S01`
- Required NFR IDs:
  - `NFR-02`
  - `NFR-06`
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
  - provider-neutral `P01-T02-S01` complete
- Soft dependencies acknowledged:
  - initial CI baseline complete
  - provider-neutral Helm foundation chart complete
- Parallel workstreams to coordinate with:
  - blocked `P01-T06` only for validation-surface awareness

## Expected Outputs

- Files expected to change:
  - `infra/**`
  - `docs/implementation/**`
  - `tests/**`
  - `package.json`
  - `.github/workflows/ci.yml`
  - relevant PM files
- Artifact outputs expected:
  - internal-only local dev cluster baseline
  - local Helm render and bootstrap-validation baseline
  - narrowed open-question boundaries for local development
- Tests or validations required:
  - `pnpm check:py`
  - `pnpm check:web`
  - Terraform validation for `infra/terraform/environments/dev`
  - Helm validation for the local target values
  - local cluster bootstrap validation if the required local tools are available

## Acceptance Criteria

- Criterion 1:
  - the repository defines one explicit internal-only local self-managed dev target that is compatible with the architecture's self-managed Kubernetes requirement and does not masquerade as a higher-environment provider choice
- Criterion 2:
  - the local target encodes the architecture's logical `general`, `stateful`, and `gpu` workload roles in a way that is inspectable and testable for development use
- Criterion 3:
  - PM and implementation docs make the local-target scope, unresolved higher-environment questions, and validation boundaries explicit

## Handoff Requirements

- Summary of work completed:
  - record the local target definition, validation path, and any open-question narrowing
- Validation performed:
  - record all local commands rerun after the local-target baseline lands
- Risks introduced or discovered:
  - record any false-readiness, resource-envelope, or local-tooling risks
- Follow-up tasks:
  - internal-only `P01-T03` continuation if the local target proves stable
  - provider-specific `P01-T02-S02` once higher-environment hosting is chosen
  - `P01-T04` state-plane work once the local target and secrets path are ready

## Current Status

- Status:
  - complete
- Summary of work completed:
  - added `infra/kind/dev-cluster.yaml` for the internal-only local cluster target
  - added `infra/helm/charts/platform-foundation/values.kind-dev.yaml` for local foundation-chart rendering
  - added local infra validation commands and repository test coverage for the local target
  - validated local cluster bootstrap, node readiness and labels, GPU taint presence, Helm lint, Helm render, and Kubernetes server-side dry-run
- Validation performed:
  - `pnpm check:py`
  - `pnpm check:web`
  - `pnpm check:infra`
  - `pnpm create:kind:dev`
  - `pnpm check:kind:nodes`
  - `kubectl get node maptheisland-dev-worker3 -o jsonpath='{.spec.taints}'`
  - `pnpm check:kind:foundation`
  - `pnpm delete:kind:dev`
- Risks introduced or discovered:
  - local `kind` validation may be mistaken for higher-environment equivalence if PM boundaries drift
