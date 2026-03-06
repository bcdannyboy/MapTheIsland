# MapTheIsland

MapTheIsland is a provenance-first document mapping and analyst workbench
platform for the public DOJ Epstein corpus.

The repository is intentionally being built in architecture order:

- Phase 00 establishes the contract, policy, and engineering baseline
- later phases add platform substrate, evidence ingest, policy enforcement,
  semantics, retrieval, BFF orchestration, UI, and controlled QA

## Current State

The repository currently contains:

- the architecture source in `Architecture_Plan.md`
- the persistent PM workspace in `pm/`
- the implementation baseline in `docs/implementation/`
- executable shared schema, contract, and policy packages in `libs/`
- the frontend workspace baseline in `apps/web`
- a provider-neutral infrastructure baseline in `infra/terraform` and
  `infra/helm`
- an internal-only local self-managed dev cluster target in `infra/kind`
- an internal-only Local control-plane baseline for Argo CD, Vault, External
  Secrets, and cert-manager in `infra/gitops` and `infra/helm/values`

Most runtime services are still reserved but unimplemented while the repository
transitions from the completed Phase 00 baseline into Phase 01 scaffolding.

## Repository Layout

```text
/infra
/services
/apps
/libs
/docs/implementation
/pm
```

See `docs/implementation/engineering-standards-baseline.md` and
`docs/implementation/service-boundaries-and-contracts.md` for the authoritative
implementation rules behind that layout.

## Python Bootstrap

Python dependency locking and local bootstrap are managed with `uv`.

```bash
uv sync --dev
uv run ruff check .
uv run mypy libs/schemas/src libs/contracts/src libs/policy/src tests
uv run pytest
```

## Frontend Bootstrap

The frontend workspace is managed with `pnpm`.

```bash
pnpm install
pnpm typecheck:web
pnpm test:web:unit
pnpm test:web:e2e
```

`apps/web` is still configuration-only in the current baseline, so browser
tests become gating once route code exists.

## Infrastructure Bootstrap

The current infrastructure baseline supports:

```bash
pnpm check:infra
pnpm check:control-plane
pnpm create:kind:dev
pnpm check:kind:nodes
pnpm check:kind:foundation
pnpm delete:kind:dev
```

The `kind` target is authoritative for Local only. It does not imply a
staging, pilot, or production hosting decision.

## Infrastructure Validation

Phase 01 infrastructure validation is now expressed at the repository root:

```bash
pnpm check:infra
```

For the internal-only local development target, the cluster bootstrap flow is:

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
pnpm apply:kind:argocd:gitops
pnpm check:kind:argocd:remote-reconciliation
pnpm check:kind:nodes
pnpm delete:kind:dev
```

This local `kind` target narrows development only. It does not select or imply
the higher-environment hosting provider.

## PM And Implementation Docs

New sessions should start with:

1. `pm/README.md`
2. `pm/11_status_dashboard.md`
3. `docs/implementation/README.md`

Material repository changes must update the PM and implementation docs in the
same session.
