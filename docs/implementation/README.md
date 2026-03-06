# Implementation Baseline

This directory holds the executable Phase 00 implementation baseline that turns
the architecture and PM system into concrete repository artifacts.

## Current Documents

- [`implementation-spec-baseline.md`](./implementation-spec-baseline.md):
  service, repository, contract, and quality baseline for initial
  implementation.
- [`service-boundaries-and-contracts.md`](./service-boundaries-and-contracts.md):
  detailed `P00-T04` service catalog, API inventory, async event inventory,
  shared-library ownership model, and contract versioning rules.
- [`policy-taxonomy-and-safety-model.md`](./policy-taxonomy-and-safety-model.md):
  detailed `P00-T03` sensitivity taxonomy, role/export matrix, prohibited-flow
  catalog, and policy-verification matrix.
- [`engineering-standards-baseline.md`](./engineering-standards-baseline.md):
  detailed `P00-T05` repository, toolchain, CI, review, and bootstrap
  standards.
- [`platform-foundation-baseline.md`](./platform-foundation-baseline.md):
  provider-neutral `P01-T02` Terraform, Helm, node-pool, naming, and storage
  baseline for the platform control plane.
- [`local-dev-platform-target.md`](./local-dev-platform-target.md):
  internal-only self-managed local cluster target that narrows `OQ-01` and the
  safe local portion of `OQ-02` without making higher-environment claims.
- [`control-plane-gitops-secrets-and-certs-baseline.md`](./control-plane-gitops-secrets-and-certs-baseline.md):
  internal-only `P01-T03` baseline for Argo CD, Vault plus External Secrets,
  cert-manager, and the local secret or certificate delivery model.
- [`architecture-traceability-matrix.md`](./architecture-traceability-matrix.md):
  section-by-section mapping from the architecture to PM workstreams and repo
  artifacts.
- [`open-implementation-gaps.md`](./open-implementation-gaps.md):
  unresolved implementation details, external decision dependencies, and safe
  continuation boundaries.

## Usage

- Treat these files as the working implementation layer for `P00-T01`.
- Update them in the same session as any change to service boundaries, contract
  publication strategy, or hard quality gates.
- Use the detailed `P00-T03`, `P00-T04`, and `P00-T05` baselines as the
  authoritative implementation layer for Phase 01 scaffolding.
- Use the Local platform and control-plane baselines as the authority for
  internal-only Phase 01 cluster work before any higher-environment target is
  chosen.
- Keep the PM dashboard, backlog, and decision log aligned with material
  changes here.
