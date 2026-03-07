# Phase 01 - Platform Foundation And Control Plane

Status: active

## Objective

Build the reproducible platform substrate, delivery pipelines, and access-control foundation required for all later work.

## Architecture Traceability

- `Architecture_Plan.md` lines 22-58
- `Architecture_Plan.md` lines 60-95
- `Architecture_Plan.md` lines 245-259
- `Architecture_Plan.md` lines 456-462

## Entry Criteria

- Phase 00 implementation contracts accepted
- open deployment and governance blockers either resolved or isolated

## Exit Criteria

- repo scaffold exists
- IaC and GitOps baseline exist
- core stateful services exist
- orchestration, eventing, model gateway, CI, observability, and auth baselines exist

## Phase Handoff Summary

- Consumes:
  - Phase 00 implementation and contract baselines
- Produces:
  - deployable cluster and delivery substrate
  - stateful-service baseline
  - orchestration and event baseline
  - auth and observability baseline
- Blocking open questions:
  - OQ-01 deployment environment
  - OQ-02 budget and capacity envelope
  - OQ-03 restricted-role governance for auth details that affect policy integration
- Primary workstreams:
  - WS-01 Platform And Infrastructure
  - WS-02 Data Plane And Orchestration
- Primary signoff roles:
  - platform lead
  - data plane lead
  - architecture lead for contract-sensitive components
- Earliest safe parallel starts:
  - Phase 02 may start once object storage, lakeFS, PostgreSQL, and Dagster are operational

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P01-T01 | done | P00-T04, P00-T05 |
| P01-T02 | active | P00-T04 |
| P01-T03 | done | P01-T02 |
| P01-T04 | active | P01-T02, P01-T03, P00-T02 |
| P01-T05 | planned | P01-T04 |
| P01-T06 | blocked | P01-T01 |
| P01-T07 | planned | P01-T02, P00-T03 |

## P01-T01 Scaffold Monorepo And Shared Libraries

- Status: done
- Relevant constraints: AC-05, AC-16, AC-17
- Objective: create the repo structure and shared library layout required by the architecture.
- Dependencies: blocking on P00-T04 and P00-T05
- Parallelization: parallelizable with P01-T02 and P01-T06
- Required external decisions: none
- Deliverables:
  - repo directory skeleton
  - shared library skeletons
  - workspace manifests
- Acceptance criteria:
  - repo layout mirrors architecture service boundaries
  - shared contract locations are defined
  - new services can be added without structural churn
- Completion note:
  - The top-level directory skeleton from Phase 00 is now reinforced by
    executable `libs/contracts` and `libs/policy` packages, repository-level
    validation updates for the expanded shared-library source roots, and
    explicit ownership or contribution guidance in `libs/` and `services/`.
- Subtasks:
  1. `P01-T01-S01` Create the top-level directories for infra, services, apps, and libs.
     Depends on: P00-T05-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T02-S01
     Concrete output: monorepo skeleton
  2. `P01-T01-S02` Create shared library placeholders for contracts, schemas, policy, prompts, and evaluation.
     Depends on: P01-T01-S01, P00-T04-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S01
     Concrete output: shared-lib skeletons
  3. `P01-T01-S03` Add workspace configuration for Python and frontend packages.
     Depends on: P01-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S02
     Concrete output: workspace manifests
  4. `P01-T01-S04` Document ownership boundaries and contribution paths for each top-level area.
     Depends on: P01-T01-S02, P01-T01-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: ownership map

## P01-T02 Provision IaC And Kubernetes Baseline

- Status: active
- Relevant constraints: AC-13, AC-15, AC-17
- Objective: provision the base platform environment using declarative infrastructure and a self-managed Kubernetes baseline.
- Dependencies: blocking on P00-T04
- Parallelization: parallelizable with P01-T01 and P01-T03
- Required external decisions: OQ-01 and OQ-02 for provider-specific implementation; provider-neutral scaffolding may proceed under the documented fallback
- Deliverables:
  - Terraform baseline
  - Kubernetes cluster baseline
  - networking and storage-class baseline
- Acceptance criteria:
  - target environment is provisionable from code
  - cluster baseline is reproducible
  - node-pool model supports general, stateful, and GPU workloads
- Current execution note:
  - the first slice was intentionally limited to provider-neutral Terraform module contracts, Helm control-plane scaffolding, naming and storage intent, and repository-level validation that locks those declarative baselines
  - the completed follow-on slice now narrows `OQ-01` and `OQ-02` only far enough to define an internal-only self-managed local development target; it does not choose a staging, pilot, or production provider
  - provider-specific cluster resources, IAM bindings, DNS integration, and higher-environment storage-class implementation remain blocked on `OQ-01` and `OQ-02`, but internal-only `P01-T03` work is now safe to begin
- Current implementation note:
  - the first provider-neutral baseline now exists under `infra/terraform/` and `infra/helm/`, with a `dev` blueprint, explicit module boundaries, logical node-pool aliases, logical storage-profile aliases, and repository tests that lock provider neutrality
  - the local-only follow-on now exists under `infra/kind/` and `infra/helm/charts/platform-foundation/values.kind-dev.yaml`, with repository commands and validations that prove cluster bootstrap, logical pool simulation, and Helm dry-run rendering against a live API server
- Subtasks:
  1. `P01-T02-S01` Define environment modules for networking, storage, DNS, IAM, and cluster resources.
     Depends on: P00-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T01-S01
     Concrete output: Terraform module map
  2. `P01-T02-S02` Provision the base Kubernetes cluster and node pools.
     Depends on: P01-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T03-S01
     Concrete output: cluster baseline
  3. `P01-T02-S03` Define storage classes, persistent-volume patterns, and environment naming conventions.
     Depends on: P01-T02-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T04-S01
     Concrete output: storage and naming standards
  4. `P01-T02-S04` Validate repeatable environment bootstrap.
     Depends on: P01-T02-S02, P01-T02-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: bootstrap validation record
- Current subtask state:
  - `P01-T02-S01` is complete in provider-neutral form through the published Terraform module map
  - `P01-T02-S02` is complete for the internal-only local self-managed dev target; provider-specific resource implementation remains blocked until `OQ-01` and `OQ-02` narrow further
  - `P01-T02-S03` is complete for local-dev naming and alias mapping, while higher-environment storage-class implementation remains blocked
  - `P01-T02-S04` is complete for local bootstrap validation through `kind` cluster creation, node readiness and labeling checks, Helm lint, and Kubernetes server-side dry-run rendering; higher-environment repeatable bootstrap remains blocked until the hosting target is explicit

## P01-T03 Configure GitOps, Secrets, And Certificate Management

- Status: done
- Relevant constraints: AC-15, AC-17
- Objective: ensure deployment, secrets, and certificates are managed declaratively and securely.
- Dependencies: blocking on P01-T02
- Parallelization: parallelizable with P01-T06
- Required external decisions: OQ-01 for higher-environment rollout only; internal-only local-dev implementation may proceed against the validated `kind` target
- Deliverables:
  - Argo CD baseline
  - Vault and external-secret flow baseline
  - cert-manager baseline
- Acceptance criteria:
  - cluster reconciliation is Git-driven
  - secrets are not committed to the repo
  - certificate lifecycle is automated
- Completion note:
  - the first internal-only slice now exists under `infra/gitops/`,
    `infra/helm/values/control-plane/`, and
    `docs/implementation/control-plane-gitops-secrets-and-certs-baseline.md`
  - Local validation now proves Argo CD installation plus server-side bootstrap
    acceptance, Local-only Vault and External Secrets secret delivery, and
    Local-only cert-manager certificate issuance through a sample workload path
  - tracked-remote Local Git reconciliation is now validated from the public
    `main` branch through the published `pnpm apply:kind:argocd:gitops` and
    `pnpm check:kind:argocd:remote-reconciliation` commands
  - higher-environment GitOps, secret, and certificate rollout remains blocked
    on `OQ-01` and `OQ-02`
- Current subtask state:
  - `P01-T03-S01` is complete for Local Argo CD installation, `AppProject`
    publication, root-bootstrap manifest publication, server-side validation,
    and tracked-remote Git reconciliation from the public `main` branch
  - `P01-T03-S02` is complete for the Local Vault plus External Secrets path,
    including gitignored bootstrap-token generation and namespace-local secret
    materialization
  - `P01-T03-S03` is complete for the Local cert-manager self-signed baseline
    and namespace-local certificate ownership model
  - `P01-T03-S04` is complete for the Local sample secret and certificate
    consumer through both the direct Local validation path and the tracked-remote
    Git reconciliation path
- Subtasks:
  1. `P01-T03-S01` Install and configure Argo CD for environment reconciliation.
     Depends on: P01-T02-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T02-S03
     Concrete output: GitOps baseline
  2. `P01-T03-S02` Define Vault and External Secrets integration path.
     Depends on: P01-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S01
     Concrete output: secret-management baseline
  3. `P01-T03-S03` Configure cert-manager and certificate ownership model.
     Depends on: P01-T03-S01
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: certificate baseline
  4. `P01-T03-S04` Verify secrets and certificate paths through a sample service deployment.
     Depends on: P01-T03-S02, P01-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S03
     Concrete output: secure deploy validation

## P01-T04 Stand Up Core Stateful Services And Catalogs

- Status: active
- Relevant constraints: AC-04, AC-13, AC-15, AC-16
- Objective: stand up the platform’s persistent state plane and catalog surfaces.
- Dependencies: blocking on P01-T02, P01-T03, and P00-T02
- Parallelization: parallelizable with P01-T05
- Required external decisions: OQ-01 and OQ-02 for higher-environment rollout; internal-only local-dev scaffolding may proceed now that `P01-T03` has established the required direct and tracked-remote control-plane path
- Deliverables:
  - object storage and lakeFS
  - PostgreSQL
  - Kafka
  - OpenSearch
  - Neo4j
  - Trino and Iceberg catalog
- Acceptance criteria:
  - each stateful service is deployable and health-checkable
  - Iceberg catalog can be reached
  - service credentials are delivered securely
- Current execution note:
  - the first bounded Local slice is now opened through
    `pm/work-packages/P01-T04-local-storage-and-postgresql-baseline.md`
  - that slice is intentionally limited to the earliest `P01-T04-S01` and
    `P01-T04-S02` surfaces needed for Local ingest replay and operational
    metadata, while higher-environment rollout remains blocked on `OQ-01` and
    `OQ-02`
- Subtasks:
  1. `P01-T04-S01` Stand up object storage and lakeFS with branchable data access.
     Depends on: P01-T02-S03, P01-T03-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T04-S02
     Concrete output: evidence storage baseline
  2. `P01-T04-S02` Stand up PostgreSQL and enable schema-management flow.
     Depends on: P01-T02-S03, P01-T03-S02, P00-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T04-S01
     Concrete output: operational metadata baseline
  3. `P01-T04-S03` Stand up Kafka, OpenSearch, Neo4j, and Trino with initial namespace and credential scaffolding.
     Depends on: P01-T04-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T05-S01
     Concrete output: event/search/graph/query baseline
  4. `P01-T04-S04` Validate catalog and service connectivity from controlled service accounts.
     Depends on: P01-T04-S01, P01-T04-S02, P01-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: state-plane validation record

## P01-T05 Establish Orchestration, Eventing, And Model Gateway Baseline

- Status: planned
- Relevant constraints: AC-16, AC-17
- Objective: establish Dagster, core event flow, and the model-gateway baseline for later services.
- Dependencies: blocking on P01-T04
- Parallelization: parallelizable with P01-T06
- Required external decisions: OQ-02 if model-hosting budget is constrained
- Deliverables:
  - Dagster baseline
  - initial event topics
  - LiteLLM or gateway baseline
- Acceptance criteria:
  - assets can be declared and materialized
  - services can emit and consume a baseline event
  - model traffic can be routed through a unified gateway surface
- Subtasks:
  1. `P01-T05-S01` Install and configure Dagster with baseline asset namespaces.
     Depends on: P01-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T04-S03
     Concrete output: orchestration baseline
  2. `P01-T05-S02` Define baseline Kafka topics and event schemas for ingest and review flows.
     Depends on: P01-T04-S03, P00-T04-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T05-S01
     Concrete output: event baseline
  3. `P01-T05-S03` Stand up the model gateway baseline and establish service-only access rules.
     Depends on: P01-T04-S04, P00-T03-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: model-gateway baseline
  4. `P01-T05-S04` Validate one sample asset flow and one sample event flow end to end.
     Depends on: P01-T05-S01, P01-T05-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: control-plane smoke test

## P01-T06 Establish CI/CD, Linting, Test, And Observability Skeleton

- Status: blocked
- Relevant constraints: AC-17, AC-18
- Objective: create the baseline engineering feedback loops required before major implementation begins.
- Dependencies: blocking on P01-T01
- Parallelization: parallelizable with P01-T03 and P01-T05
- Required external decisions: none
- Deliverables:
  - CI pipeline baseline
  - lint/type/test baseline
  - OpenTelemetry, Prometheus, and Grafana baseline
- Acceptance criteria:
  - code quality checks run automatically
  - baseline service metrics are collectible
  - failures are visible early
- Current implementation note:
  - `P01-T06-S01` and `P01-T06-S02` are now complete through the initial
    repository CI workflow and root workspace-check commands.
  - `P01-T06-S03` and `P01-T06-S04` remain blocked on `P01-T04-S04` because
    no runtime service or state-plane observability target exists yet.
- Subtasks:
  1. `P01-T06-S01` Configure baseline CI jobs for formatting, linting, typing, and unit tests.
     Depends on: P01-T01-S03, P00-T05-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T03-S02
     Concrete output: CI baseline
  2. `P01-T06-S02` Configure frontend and backend workspace build checks.
     Depends on: P01-T01-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S01
     Concrete output: workspace build checks
  3. `P01-T06-S03` Configure baseline tracing, metrics, and dashboard collection.
     Depends on: P01-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T03-S04
     Concrete output: observability baseline
  4. `P01-T06-S04` Publish service bootstrap and developer verification instructions.
     Depends on: P01-T06-S01, P01-T06-S02, P01-T06-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: engineering bootstrap doc

## P01-T07 Establish Identity And Access Foundation

- Status: planned
- Relevant constraints: AC-09, AC-15
- Objective: establish OIDC authentication and the foundation for role-based policy enforcement.
- Dependencies: blocking on P01-T02 and P00-T03
- Parallelization: parallelizable with P01-T06
- Required external decisions: OQ-03, OQ-04
- Deliverables:
  - Keycloak baseline
  - role mapping baseline
  - token validation baseline
- Acceptance criteria:
  - service and user identity flows are separate
  - baseline roles exist even if final restricted governance is pending
  - BFF integration path is clear
- Subtasks:
  1. `P01-T07-S01` Stand up the OIDC provider baseline and define client/application registration flow.
     Depends on: P01-T02-S04, P00-T03-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S01
     Concrete output: auth provider baseline
  2. `P01-T07-S02` Define initial human and service role mappings.
     Depends on: P01-T07-S01, P00-T03-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: role mapping draft
  3. `P01-T07-S03` Define BFF-side token validation and identity propagation rules.
     Depends on: P01-T07-S01, P00-T04-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T01-S01 later
     Concrete output: auth integration contract
  4. `P01-T07-S04` Validate a protected sample endpoint and service account path.
     Depends on: P01-T07-S02, P01-T07-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: identity foundation smoke test
