# Platform Foundation Baseline

## Purpose

This document is the provider-neutral `P01-T02` implementation baseline for the
MapTheIsland control plane. It fixes the Terraform and Helm structure that later
Phase 01 infrastructure work must inherit without prematurely choosing a
provider, network perimeter, IAM backend, or storage-class implementation.

## Slice Boundary

This baseline intentionally resolves only the safe, reusable parts of
`P01-T02`:

- Terraform module boundaries for networking, storage, DNS, identity, and
  cluster intent
- environment-blueprint structure for the `dev` environment
- logical node-pool and workload-priority roles
- logical storage-profile aliases
- namespace conventions for control-plane, data-plane, and application
  workloads

This baseline explicitly does not resolve:

- the hosting target named in `OQ-01`
- budget-specific sizing or throughput claims from `OQ-02`
- provider-specific IAM, DNS, backup, or storage wiring
- GitOps, secrets, certificate, or stateful-service implementation

The local-only follow-on to this baseline is documented separately in
`docs/implementation/local-dev-platform-target.md`. That document narrows local
development only and does not alter the unresolved higher-environment provider
decision.

## Provider-Neutral Rules

- Terraform code in this slice may define variables, locals, outputs, and
  module wiring.
- Terraform code in this slice may not commit provider-specific resources.
- Helm code in this slice may create cluster-neutral objects such as namespaces,
  priority classes, and baseline config surfaces.
- Helm code in this slice may not assume one ingress controller, CSI driver,
  secret operator, or cloud load balancer.
- Logical storage profiles are named aliases only. They are not concrete
  `StorageClass` objects yet.

## Terraform Layout

The provider-neutral Terraform structure is:

```text
infra/terraform/
  versions.tf
  environments/
    dev/
  modules/
    networking/
    storage/
    dns/
    identity/
    cluster/
```

### Module Responsibilities

| Module | Responsibility In This Slice | Explicit Deferrals |
| --- | --- | --- |
| `networking` | define CIDR, service-network, egress, and ingress intent | provider VPC/VNet resources, firewall rules, NAT, load balancers |
| `storage` | define object-store, backup, and logical storage-profile intent | provider bucket resources, CSI-backed storage classes, retention enforcement |
| `dns` | define zone ownership and endpoint-intent metadata | registrar integration, hosted-zone creation, ingress record management |
| `identity` | define namespace, service-account, and secret-delivery intent | workload identity bindings, Vault auth backend, cloud IAM roles |
| `cluster` | define Kubernetes version, namespace prefix, and node-pool intent | managed-node resources, autoscaling groups, GPU images, OS-specific tuning |

## Environment Blueprint

The initial environment blueprint is `infra/terraform/environments/dev/`.

It exists to make one environment contract inspectable and reproducible without
claiming that it can already provision a real target. The `dev` blueprint fixes
the baseline naming and pool semantics that later provider-specific work must
consume.

## Logical Node-Pool Model

The architecture requires three workload classes:

| Pool Alias | Purpose | Allowed Workload Examples |
| --- | --- | --- |
| `general` | stateless CPU-oriented services | BFF, orchestration web services, lightweight indexing helpers |
| `stateful` | persistent SSD-backed services | PostgreSQL, Kafka, OpenSearch, Neo4j, Trino coordinator, lakeFS control plane |
| `gpu` | accelerator-backed heavy inference or OCR | OCR recovery, embedding generation, reranking experiments, self-hosted models |

The current baseline captures these as logical pool contracts and cluster
priority intent only. Concrete instance types, taints, labels, storage devices,
and autoscaling rules are deferred.

## Logical Storage Profiles

The provider-neutral storage aliases are:

| Alias | Intended Use | Current Meaning |
| --- | --- | --- |
| `general` | general-purpose persistent or semi-persistent volumes | default non-specialized storage profile |
| `stateful_ssd` | latency-sensitive persistent state | logical alias for SSD-backed stateful workloads |
| `gpu_scratch` | high-throughput ephemeral or checkpoint-adjacent scratch | logical alias for accelerator-adjacent temporary work |

These aliases are contractual names only. They become concrete storage classes
after the provider decision is made.

## Helm Baseline

The first Helm chart is `infra/helm/charts/platform-foundation`.

Its purpose is to publish cluster-neutral platform intent:

- namespace creation for control-plane, data-plane, and application surfaces
- workload-priority classes aligned to the node-pool model
- values-schema validation for the chart inputs

This chart is not a deployment of runtime services. It is the cluster-baseline
contract that later Argo CD and service charts will inherit.

## Unresolved Boundaries

- `OQ-01` still blocks provider-specific Terraform resources and cluster
  bootstrapping.
- `OQ-02` still blocks authoritative sizing, persistence, and capacity claims.
- `GAP-011`, `GAP-012`, `GAP-013`, `GAP-014`, and `GAP-015` remain open and
  should constrain later Phase 01 work.

## Validation Expectation

Until direct Terraform and Helm tool validation becomes a stable repository
baseline, this slice is locked by repository tests that assert:

- the Terraform module map exists
- provider-specific resources have not been introduced
- the environment blueprint wires all required modules
- the Helm foundation chart and values schema exist
- CI watches the `infra/` surface

The local-dev follow-on extends that validation with:

- `kind` cluster bootstrap from `infra/kind/dev-cluster.yaml`
- Helm lint and render checks using `values.kind-dev.yaml`
- Kubernetes API dry-run validation against the local cluster
- root command publication through `pnpm check:infra`,
  `pnpm create:kind:dev`, `pnpm check:kind:nodes`,
  `pnpm check:kind:foundation`, and `pnpm delete:kind:dev`

## References

- `Architecture_Plan.md`, sections 2 through 4
- `pm/backlog/phase-01-platform-foundation.md`
- `pm/research/open-questions.md`
- `docs/implementation/engineering-standards-baseline.md`
