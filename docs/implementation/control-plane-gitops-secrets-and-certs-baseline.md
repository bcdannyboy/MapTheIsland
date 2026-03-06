# Control Plane GitOps, Secrets, And Certificates Baseline

## Purpose

This document defines the first internal-only `P01-T03` implementation
baseline for MapTheIsland. It builds on the validated local `kind` target and
publishes the local control-plane rules for GitOps, secret delivery, and
certificate ownership without making higher-environment claims.

This baseline also narrows the local portion of `GAP-012` by defining:

- the operator namespace boundary
- the secret bootstrap trust chain for Local
- the service-scoped secret-materialization rule
- the certificate ownership model for Local

## Slice Boundary

This baseline is authoritative for `Local` development only.

It is not authoritative for:

- shared `Dev`
- `Staging`
- `Pilot`
- `Production`

It does not choose a higher-environment hosting target, Vault auth backend,
external certificate authority, ingress controller, or DNS integration.

## Local Control Plane Topology

The local control plane is organized into these layers:

1. `platform-foundation` creates the namespace and priority baseline.
2. Argo CD owns the GitOps reconciliation contract for Local.
3. Vault remains the secret system of record for Local.
4. External Secrets Operator delivers namespace-local runtime secrets from
   Vault into consuming namespaces.
5. cert-manager owns certificate issuance and renewal for Local TLS objects.

All control-plane operators run in
`maptheisland-dev-foundation-system`.

Runtime secret and certificate targets do not remain in that namespace unless
the consuming workload also lives there. Application workloads receive their
own Kubernetes Secret objects in their own namespaces.

## GitOps Model

The Local GitOps baseline uses Argo CD with a repo-managed app-of-apps
structure:

- a root bootstrap `Application`
- one `AppProject` for the local control plane
- child `Application` manifests for:
  - `platform-foundation`
  - Argo CD self-management
  - Vault
  - External Secrets Operator
  - cert-manager
  - a sample secret-and-certificate consumer

The repository URL for Local is:

- `https://github.com/bcdannyboy/MapTheIsland.git`
- branch: `main`

This URL is public and reachable, which keeps the Local baseline aligned with a
real Git remote instead of a file-path-only shortcut.

### Important Local Validation Boundary

The current repository validation path intentionally separates two things:

- repo-managed Argo CD manifests that define the GitOps contract
- direct local Helm or `kubectl` installation steps used to validate those same
  control-plane surfaces before the new manifests are necessarily present on the
  tracked remote branch

This means:

- Local validation may install Argo CD, Vault, External Secrets Operator, and
  cert-manager directly from Helm while still validating the Argo CD manifest
  surfaces with server-side dry-run.
- Live Git reconciliation from Argo CD is authoritative only after the same
  manifests exist on the tracked remote branch.
- Direct local installation success may not be cited as evidence that full
  end-to-end Git reconciliation has already been proven.

## Namespace And Tenancy Rules

The Local namespace and tenancy model is:

- operator namespace:
  - `maptheisland-dev-foundation-system`
- control-plane observability namespace:
  - `maptheisland-dev-foundation-observability`
- application runtime namespace:
  - `maptheisland-dev-application`

The key rules are:

- control-plane operators may store their own internal working secrets in the
  operator namespace only
- Vault bootstrap token material for Local lives only in the operator namespace
  and in gitignored local state files
- service runtime secrets are synchronized only into the consuming service
  namespace
- service runtime secrets may not be shared across namespaces by reference
- certificate secrets are owned per namespace by cert-manager and are not
  shared cluster-wide

## Local Secret Bootstrap Trust Chain

The Local secret bootstrap chain is:

1. generate a gitignored local Vault dev root token under
   `.state/kind/vault-root-token`
2. install Vault in Local development mode with that generated token
3. mirror the token into a Kubernetes Secret in
   `maptheisland-dev-foundation-system`
4. define a `ClusterSecretStore` that points to Vault and reads that token
   through `tokenSecretRef`
5. seed a sample secret in Vault under the mounted `secret/` path
6. define an `ExternalSecret` in the consumer namespace that materializes only
   the required runtime key into a namespace-local Kubernetes Secret
7. define the sample workload so it depends on the namespace-local secret, not
   on direct cross-namespace reads

The root token is a Local bootstrap convenience only. It is not acceptable for
higher environments and is not committed to Git.

## Local Certificate Ownership Model

The Local certificate model is intentionally minimal:

- cert-manager is installed into `maptheisland-dev-foundation-system`
- a self-signed `ClusterIssuer` named
  `maptheisland-local-selfsigned` exists only for Local
- each consuming workload requests its own `Certificate`
- cert-manager writes the resulting TLS Secret into the same namespace as the
  `Certificate`

This baseline is sufficient to validate:

- certificate CRDs and controller wiring
- namespace-local TLS secret ownership
- workload dependence on cert-manager-managed TLS secrets

This baseline is not sufficient to claim:

- public trust
- ACME automation
- higher-environment ingress readiness
- cross-cluster trust distribution

## Local Validation Contract

The repository publishes two validation layers for this baseline.

### Cluster-Free Validation

Use:

```bash
pnpm check:control-plane
```

This validates:

- Helm repo and chart resolution for Argo CD, Vault, External Secrets, and
  cert-manager
- rendering of the pinned Local values files for those charts
- the repo-managed structure that drives the control-plane baseline

### Cluster-Backed Local Validation

Use the Local `kind` target and then apply the control-plane path:

```bash
pnpm create:kind:dev
pnpm apply:kind:foundation
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

This validates:

- Argo CD CRD availability and bootstrap-manifest server-side acceptance
- Local Vault bootstrap with non-committed token material
- External Secrets delivery into the consumer namespace
- cert-manager certificate issuance into the consumer namespace
- a sample deployment that depends on both a synchronized secret and a
  cert-manager-managed TLS Secret

### Tracked-Remote Git Reconciliation Validation

After the same repo state exists on the tracked public branch, validate the
live Local GitOps path with:

```bash
pnpm apply:kind:argocd:gitops
pnpm check:kind:argocd:remote-reconciliation
```

This validation is stronger than direct Local bootstrap because it proves:

- the Local `AppProject` and root `Application` are accepted as live objects
- Argo CD can fetch the tracked public repository state on `main`
- the child control-plane `Application` objects reconcile from that tracked
  remote state
- the sample secret and certificate consumer can become healthy after the
  Local-only Vault bootstrap material is seeded outside Git

The tracked-remote validation does not change the Local-only boundary. It still
does not claim shared-environment, pilot, or production GitOps readiness.

## Explicit Non-Goals

This baseline does not yet include:

- higher-environment Vault auth backends
- external CA or ACME issuers
- ingress or gateway routing
- sealed-secrets or SOPS
- live higher-environment Git reconciliation claims
- policy-sensitive restricted-role secret segmentation

## References

- `docs/implementation/local-dev-platform-target.md`
- `docs/implementation/platform-foundation-baseline.md`
- `docs/implementation/open-implementation-gaps.md`
- `infra/gitops/README.md`
- `pm/backlog/phase-01-platform-foundation.md`
