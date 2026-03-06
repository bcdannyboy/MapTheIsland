# Infrastructure Workspace

This directory owns the declarative platform substrate for MapTheIsland.

- `terraform/`: provider-neutral environment blueprints, module boundaries, and
  later provider-bound implementations for networking, storage, DNS, IAM, and
  cluster resources
- `helm/`: deployable charts for first-party services, platform namespaces, and
  approved dependency baselines
- `kind/`: internal-only local self-managed cluster target for development and
  validation
- `gitops/`: repo-managed Argo CD bootstrap, local application manifests, and
  sample control-plane reconciliation surfaces

## Current Phase 01 Scope

The current `P01-T02` slice is intentionally provider-neutral. It establishes:

- Terraform module boundaries and environment blueprints
- logical node-pool intent for general, stateful, and GPU workloads
- logical storage-profile aliases rather than provider-specific storage classes
- Helm baseline for namespaces and cluster-level workload priority intent

This directory still does not contain provider-specific infrastructure
resources. Hosting-target selection, DNS integrations, IAM backends, and
concrete storage classes remain blocked on `OQ-01` and `OQ-02`.

The one additional resolved boundary is local development: `infra/kind/`
defines a self-managed Docker-backed cluster target for internal-only
validation. It narrows local development only; it does not answer the
higher-environment hosting question.

`infra/gitops/` extends that Local boundary into the control-plane layer for
Argo CD, Vault, External Secrets, cert-manager, and sample secret or
certificate delivery. Those manifests are authoritative for Local only until a
higher-environment target is chosen.
