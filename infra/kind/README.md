# Local Kind Dev Target

This directory defines the internal-only self-managed Kubernetes target for
local MapTheIsland development.

## Scope

This target exists to narrow `OQ-01` for local development without pretending
that staging, pilot, or production hosting has been selected.

It is intentionally limited to:

- Docker-backed `kind` cluster bootstrap
- simulated workload pools for `general`, `stateful`, and `gpu`
- local Helm rendering and dry-run validation of the platform-foundation chart
- local control-plane validation for Argo CD, Vault, External Secrets, and
  cert-manager
- bounded local validation on one workstation

It does not claim:

- higher-environment provider selection
- real GPU availability
- production-authoritative storage, DNS, IAM, ingress, or backup behavior
- readiness for pilot or production workloads

## Cluster Model

The local target uses one control-plane node plus three worker nodes:

- `general`: CPU-oriented APIs and orchestration
- `stateful`: persistent-service simulation
- `gpu`: accelerator-adjacent workload simulation only

The `gpu` pool is simulated through labels and taints. It does not imply local
GPU hardware is present.

## Validation Flow

Use these commands from the repository root:

```bash
pnpm create:kind:dev
pnpm check:kind:nodes
pnpm apply:kind:foundation
pnpm check:kind:foundation
pnpm check:control-plane
pnpm apply:kind:argocd
pnpm check:kind:argocd:bootstrap
pnpm apply:kind:cert-manager
pnpm apply:kind:vault
pnpm bootstrap:kind:vault:sample-secret
pnpm apply:kind:external-secrets
pnpm apply:kind:sample-secret-consumer
pnpm check:kind:sample-secret-consumer
pnpm delete:kind:dev
```

## Follow-On Boundary

This directory is a local validation target only. Provider-specific Terraform,
higher-environment GitOps rollout, higher-environment secret delivery, and
stateful service installation remain later Phase 01 work and must stay aligned
to the PM decision surfaces.
