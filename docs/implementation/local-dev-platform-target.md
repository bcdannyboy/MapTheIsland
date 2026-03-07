# Local Development Platform Target

## Purpose

This document defines the internal-only self-managed development target for
MapTheIsland. It narrows `OQ-01` enough to keep Phase 01 moving locally while
preserving the unresolved higher-environment hosting choice.

It also narrows the safe local portion of `OQ-02` by fixing a small-footprint
development posture rather than leaving all capacity assumptions abstract.

## Decision Boundary

- This document is authoritative for `Local` development only.
- It is not authoritative for shared `Dev`, `Staging`, `Pilot`, or
  `Production`.
- It does not authorize cloud, on-prem, or shared-cluster claims.

## Target Definition

The local development target is:

- `kind` running on local Docker
- one control-plane node
- three worker nodes labeled for the architecture's logical workload roles:
  - `general`
  - `stateful`
  - `gpu`

The `gpu` worker is a scheduling simulation target only. No local GPU hardware
is implied or required by this baseline.

## Small-Footprint Local Capacity Posture

The local target intentionally adopts these limits:

- one-host development only
- no production-authoritative throughput claims
- no real high-availability guarantees
- storage alias collapse to simple local classes for validation only
- bounded local validation of control-plane contracts rather than full
  state-plane scale

This posture is sufficient for:

- validating namespace and priority conventions
- validating basic cluster bootstrap semantics
- validating chart rendering and cluster API compatibility
- preparing later internal-only Phase 01 state-plane and GitOps work

This posture is not sufficient for:

- production-like OCR throughput
- real GPU scheduling
- higher-environment persistence or backup claims
- pilot or production readiness statements

## Storage And Pool Mapping

The local target preserves the architecture's logical model while explicitly
collapsing its implementation:

| Logical Contract | Local Dev Mapping | Meaning |
| --- | --- | --- |
| `general` pool | labeled worker node | CPU-oriented API and orchestration simulation |
| `stateful` pool | labeled worker node | stateful workload scheduling simulation |
| `gpu` pool | labeled and tainted worker node | accelerator-adjacent scheduling simulation only |
| `general` storage alias | `standard` | default local persistent class |
| `stateful_ssd` storage alias | `standard` | local stand-in for SSD-backed stateful storage |
| `gpu_scratch` storage alias | `ephemeral` | local stand-in for accelerator scratch behavior |

## Validation Contract

The local target is considered valid when:

- the `kind` cluster can be created from `infra/kind/dev-cluster.yaml`
- the worker roles appear with the expected labels
- the foundation chart lints with `values.kind-dev.yaml`
- the rendered chart passes Kubernetes server-side dry-run against the local
  cluster

## Repository Command Surface

The repository publishes this local-dev command flow at the root:

```bash
pnpm check:infra
pnpm check:control-plane
pnpm create:kind:dev
pnpm check:kind:nodes
pnpm check:kind:foundation
pnpm check:kind:argocd:bootstrap
pnpm check:kind:sample-secret-consumer
pnpm delete:kind:dev
```

`pnpm check:infra` remains cluster-free and validates the Terraform blueprint,
the kind-specific Helm values, and chart rendering. The `create`, `nodes`,
`foundation`, and `delete` commands validate the internal-only cluster target
itself. `pnpm check:control-plane` validates the Local-only control-plane chart
values, while the `argocd` and `sample-secret-consumer` checks validate the
local bootstrap-manifest path plus the namespace-local secret and certificate
delivery path.

Local tracked-remote Git reconciliation is validated with:

```bash
pnpm apply:kind:argocd:gitops
pnpm check:kind:argocd:remote-reconciliation
```

Those commands validate the repo-managed `AppProject` and root `Application`
objects plus the child `Application` reconciliation flow from the tracked
public branch for the current repo state. They remain distinct from direct
chart installation commands and are the authoritative Local proof of Git-driven
reconciliation.

## Explicit Non-Goals

This target does not yet include:

- MinIO, lakeFS, PostgreSQL, Kafka, OpenSearch, Neo4j, or Trino
- provider-specific Terraform resources
- higher-environment GitOps, secret-delivery, or certificate claims

Argo CD, Vault, External Secrets Operator, and cert-manager are now defined for
Local in `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`.
Higher-environment rollout of those systems remains later Phase 01 work.

## References

- `docs/implementation/platform-foundation-baseline.md`
- `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`
- `infra/kind/README.md`
- `pm/research/open-questions.md`
