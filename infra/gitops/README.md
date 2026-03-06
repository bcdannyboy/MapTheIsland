# GitOps Baseline

This directory owns the repo-managed GitOps baseline for MapTheIsland.

## Current Scope

The current `P01-T03` slice is internal-only and Local-only. It publishes:

- Argo CD bootstrap manifests
- the Local control-plane `AppProject`
- Local child `Application` manifests for platform-foundation, Argo CD, Vault,
  External Secrets Operator, cert-manager, and a sample secret consumer
- the sample manifest set that exercises secret and certificate delivery into
  the application namespace

## Layout

- `bootstrap/local/`: root bootstrap manifests that are applied after Argo CD
  CRDs exist
- `applications/local/control-plane/`: child `Application` manifests reconciled
  by the root application
- `apps/local/sample-secret-consumer/`: namespace-scoped sample resources used
  to validate secret and certificate delivery

## Local Boundary

This GitOps baseline uses the public repository URL
`https://github.com/bcdannyboy/MapTheIsland.git` on branch `main`.

That keeps the desired-state contract Git-addressable for Argo CD, but the
current local validation path still distinguishes between:

- repo-managed Application manifests
- direct local installation commands used to validate those same charts and
  manifests before the new repo state is necessarily present on the tracked
  branch

Do not interpret direct local install success as proof that live Git
reconciliation has already been exercised end to end.

## Tracked-Remote Local Validation

When the current repo state is present on the tracked remote branch, validate
the live Local GitOps path with:

```bash
pnpm apply:kind:argocd:gitops
pnpm check:kind:argocd:remote-reconciliation
```

These commands are intentionally separate from direct chart installation. They
apply the repo-managed bootstrap objects and then wait for Argo CD to reconcile
the child applications from the tracked remote branch.
