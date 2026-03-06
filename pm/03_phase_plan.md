# Master Phase Plan

## Overview

The program is organized into eight phases. The order below is intentional. It follows the architecture’s requirement that immutable evidence, provenance, policy enforcement, and review infrastructure precede higher-level inference and user-facing QA.

## Phase Sequence

### Phase 00: Constraints Translation And Implementation Specification

- Objective: convert the architecture into executable contracts, schemas, policies, and service boundaries so later phases do not drift.
- Entry criteria: none.
- Exit criteria:
  - canonical evidence model defined
  - review-state and sensitivity taxonomy defined
  - service and API contract baseline created
  - repository and documentation conventions defined
  - initial risk, decision, and research registers created
- Major outputs:
  - implementation spec
  - schema contracts
  - task backlogs and dependency map
- Can run in parallel with: internal research and documentation setup.

### Phase 01: Platform Foundation And Control Plane

- Objective: stand up the reproducible infrastructure substrate and monorepo structure required for all later work.
- Entry criteria: Phase 00 baseline contracts exist.
- Exit criteria:
  - repo scaffold exists
  - IaC and GitOps baseline exist
  - object storage, lakeFS, PostgreSQL, Dagster, Kafka, and secrets baseline are operational
  - CI skeleton exists
  - auth foundation exists
- Major outputs:
  - deployable platform skeleton
  - baseline observability and delivery pipelines

### Phase 02: Immutable Ingestion And Canonical Evidence Layer

- Objective: acquire lawful source data, preserve it immutably, process files deterministically, and materialize canonical `Document`, `Page`, and `Span` assets.
- Entry criteria: Phase 01 storage and orchestration prerequisites exist.
- Exit criteria:
  - harvester/downloader path works
  - raw evidence is versioned and replayable
  - dedup and routing are operational
  - PDF, OCR, and layout processing produce canonical page/span assets
  - asset validation and lineage are functional
- Major outputs:
  - evidence layer MVP
  - ingest and docproc pipelines

### Phase 03: Policy Enforcement, Review Loops, And Adjudication

- Objective: enforce safety and review boundaries before semantic extraction becomes authoritative in workflows.
- Entry criteria: canonical evidence assets exist and auth/control-plane foundations are in place.
- Exit criteria:
  - sensitivity pass operational
  - role and policy enforcement path operational
  - review queues and adjudication persistence operational
  - audit and export controls operational
- Major outputs:
  - policy-safe evidence access model
  - review control plane

### Phase 04: Structured Extraction And Evidence-Backed Semantics

- Objective: transform spans into entities, aliases, relations, events, thread reconstructions, and redaction objects.
- Entry criteria: Phases 02 and 03 completed to the extent required by each task.
- Exit criteria:
  - entity and alias extraction operational
  - identity resolution workflow operational
  - relation and event extraction operational
  - redaction objects operational
  - event-centric semantics available for downstream systems
- Major outputs:
  - structured evidence-backed semantics

### Phase 05: Retrieval, Graph, Analytics, And Hypothesis Layer

- Objective: create search, graph, topic, temporal, and weak-supervision layers on top of the evidence-backed semantic foundation.
- Entry criteria: structured extraction outputs exist and policy boundaries are enforceable.
- Exit criteria:
  - search index and retrieval pipeline operational
  - graph materialization operational
  - analytics tables operational
  - topic and weak-supervision lanes operational with evaluation hooks
  - validation and MLflow tracking expanded
- Major outputs:
  - analyst-facing retrieval and analytics substrate

### Phase 06: Backend-For-Frontend And Evidence Workbench UI

- Objective: expose safe, inspectable analyst workflows for search, document review, entity/event exploration, and human adjudication.
- Entry criteria: backend data products and policy controls are sufficiently stable.
- Exit criteria:
  - FastAPI BFF operational
  - Next.js shell operational
  - search, document viewer, entity, event, review, and job flows operational
  - policy context and provenance summary exposed through APIs
- Major outputs:
  - evidence workbench MVP

### Phase 07: Controlled QA, Advanced Analytics UI, And Production Hardening

- Objective: add controlled QA, advanced graph/topic/timeline views, deeper evaluation, SLO-based operations, and release hardening.
- Entry criteria: evidence workbench MVP operational and quality gates active.
- Exit criteria:
  - controlled QA operational with citations, support states, and abstention
  - advanced analytics and restricted features operational under policy
  - release criteria satisfied for pilot or production milestone
- Major outputs:
  - full analyst platform

## Critical Path

The explicit critical path is:

`P00 -> P01 -> P02 -> P03 -> P04 -> P05 (minimum retrieval/graph/search) -> P06 (evidence workbench MVP) -> P07`

The first release boundary is after the minimum viable subset of Phase 06, not after Phase 07.

## Parallel Work Model

The largest safe parallel lanes are:

- implementation spec and documentation
- infrastructure and CI/CD
- document processing and evidence persistence
- policy and review infrastructure
- semantic extraction and resolution
- retrieval, graph, and analytics
- BFF and UI
- evaluation and release engineering

These lanes are cross-referenced in [`05_workstream_index.md`](./05_workstream_index.md).

## Release Milestones

- Milestone M0: planning baseline and implementation spec complete
- Milestone M1: platform and evidence substrate complete
- Milestone M2: policy-safe evidence workbench MVP complete
- Milestone M3: restricted analyst preview complete
- Milestone M4: controlled QA and advanced analytics complete
- Milestone M5: production readiness complete

## References

- [`Architecture_Plan.md`](../Architecture_Plan.md): lines 22-109, 111-171, 173-243, 245-289, 293-462, 470
- Verified supporting documentation in [`08_research_register.md`](./08_research_register.md)
