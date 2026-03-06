# Work Package

## Header

- Work package ID: `WP-P01-T02-001`
- Date: 2026-03-06
- Related task ID: `P01-T02`
- Owner: platform or infrastructure lead
- Reviewer: architecture lead, data and orchestration lead

## Scope

- Objective:
  - Execute the first safe `P01-T02` slice by publishing a provider-neutral Terraform and Helm baseline that fixes module boundaries, environment naming intent, node-pool intent, storage-pattern intent, and bootstrap-validation expectations without assuming a concrete hosting provider.
- In scope:
  - provider-neutral Terraform module map for networking, storage, DNS, IAM, and cluster resources
  - provider-neutral environment blueprints that express cluster, naming, and workload-pool intent without binding to one provider
  - Helm baseline for cluster namespaces and first-party control-plane deployment conventions that are safe before Argo CD, Vault, and cert-manager land
  - repository tests that lock the new declarative baseline and verify provider-neutral boundaries
  - PM and implementation-doc reconciliation required to record the new infra baseline
- Explicitly out of scope:
  - provider-specific Terraform resources
  - actual cluster provisioning in a named environment
  - Argo CD, Vault, External Secrets Operator, or cert-manager implementation
  - live stateful-service deployment
  - ingress, IAM, storage-class, DNS, or backup integrations that assume a chosen provider

## Inputs

- Required files:
  - `pm/backlog/phase-01-platform-foundation.md`
  - `pm/11_status_dashboard.md`
  - `pm/research/open-questions.md`
  - `docs/implementation/implementation-spec-baseline.md`
  - `docs/implementation/service-boundaries-and-contracts.md`
  - `docs/implementation/engineering-standards-baseline.md`
  - `docs/implementation/open-implementation-gaps.md`
  - `infra/README.md`
  - `infra/terraform/README.md`
  - `infra/helm/README.md`
- Required artifact IDs:
  - none newly introduced
- Required upstream tasks:
  - `P00-T04`
- Required contracts or schemas:
  - service-boundary baseline
  - environment and promotion model
  - provider-neutral fallback for `OQ-01`
- Required NFR IDs:
  - `NFR-02`
  - `NFR-06`
  - `NFR-07`
  - `NFR-11`
  - `NFR-13`
- Required decision IDs or open-question IDs:
  - `D-002`
  - `D-003`
  - `D-010`
  - `OQ-01`
  - `OQ-02`
- Required research or decisions:
  - current Kubernetes and Terraform provider-neutral baseline only; do not introduce provider-specific external research in this slice

## Dependency Statement

- Hard dependencies confirmed:
  - `P00-T04` complete
- Soft dependencies acknowledged:
  - `P01-T01` shared-library and repo baseline complete
  - `P01-T06-S01/S02` CI baseline complete
- Parallel workstreams to coordinate with:
  - blocked `P01-T06` observability follow-on only for documentation awareness

## Expected Outputs

- Files expected to change:
  - `infra/terraform/**`
  - `infra/helm/**`
  - `tests/**` if repository tests are added for infra surfaces
  - relevant PM and implementation docs
- Artifact outputs expected:
  - provider-neutral Terraform baseline
  - provider-neutral Helm control-plane baseline
  - repository-level validation for declarative infra boundaries
- Handoff target workstream:
  - `WS-01 Platform And Infrastructure`
- Tests or validations required:
  - `pnpm check:py`
  - `pnpm check:web`
  - any additional repository tests that lock the new infra baseline
- Documentation updates required:
  - Phase 01 backlog
  - status dashboard
  - session log
  - implementation docs for infra and cluster-baseline guidance
  - open-gap or decision surfaces if the scope of `OQ-01` is narrowed

## Acceptance Criteria

- Criterion 1:
  - provider-neutral Terraform modules and environment blueprints exist for networking, storage, DNS, IAM, and cluster intent without binding to one cloud or on-prem provider.
- Criterion 2:
  - Helm baseline exists for namespaces, naming, and first-party control-plane conventions that later GitOps and stateful-service work can inherit.
- Criterion 3:
  - repository tests and documentation make the new declarative baseline inspectable, reproducible, and explicit about what remains unresolved.

## Handoff Requirements

- Summary of work completed:
  - record the Terraform module map, Helm baseline, and repository validation surfaces added
- Validation performed:
  - record all local commands rerun after the infra baseline lands
- Risks introduced or discovered:
  - record any tooling, environment, or provider-neutral abstraction risk
- Follow-up tasks:
  - provider-specific `P01-T02-S02` once `OQ-01` narrows
  - `P01-T03`
  - `P01-T04`
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - risk register or decision log if the infrastructure baseline introduces a durable rule

## Current Status

- Status:
  - complete for the provider-neutral `P01-T02` slice; overall task remains active for later provider-specific follow-on work
- Summary of work completed:
  - added provider-neutral Terraform module contracts for networking, storage, DNS, identity, and cluster intent
  - added a provider-neutral `dev` environment blueprint and example variables
  - added the `platform-foundation` Helm chart for namespaces and workload-priority intent
  - added repository tests that lock provider neutrality and infra baseline file surfaces
  - updated implementation docs, PM state, and CI path coverage for `infra/**`
- Validation performed:
  - `pnpm check:py`
  - `pnpm check:web`
  - `terraform fmt -recursive infra/terraform`
  - `terraform fmt -check -recursive infra/terraform`
  - `terraform init -backend=false`
  - `terraform validate`
- Risks introduced or discovered:
  - provider-neutral blueprints may be mistaken for deploy-ready infrastructure if PM boundaries drift
- Follow-up tasks:
  - narrow `OQ-01` and `OQ-02`
  - execute provider-specific `P01-T02-S02`
  - continue `P01-T03`
  - continue `P01-T04`
- Required PM updates:
  - backlog
  - dashboard
  - session log
  - decision log
  - risk register
