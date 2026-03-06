# Workstream Index

This document groups the plan by durable ownership lane rather than by phase. It exists so multiple senior contributors or subagents can work in parallel without losing architectural coherence.

## WS-01 Platform And Infrastructure

- Owner archetype:
  - platform lead
- Scope:
  - monorepo scaffold
  - IaC
  - Kubernetes and GitOps
  - secrets, certificates, networking
  - baseline CI/CD
- Primary tasks:
  - P01-T01
  - P01-T02
  - P01-T03
  - P01-T06
  - portions of P01-T07
- Main outputs:
  - deployable cluster baseline
  - reproducible engineering toolchain
  - delivery pipelines
- Accountable artifacts:
  - repo skeleton
  - Kubernetes baseline
  - Argo CD baseline
  - secret and certificate delivery path
- Primary dependencies:
  - P00-T04
  - P00-T05
- Hands off to:
  - WS-02 for stateful-service and catalog deployment
  - WS-03 for evidence ingestion runtime

## WS-02 Data Plane And Orchestration

- Owner archetype:
  - data plane lead
- Scope:
  - object storage and lakeFS
  - Iceberg catalog
  - PostgreSQL
  - Kafka
  - Dagster
  - Trino
  - model gateway baseline
- Primary tasks:
  - P01-T04
  - P01-T05
  - P02-T05
- Main outputs:
  - operational platform substrate
  - versioned analytical asset control plane
- Accountable artifacts:
  - raw evidence system of record
  - Iceberg catalog baseline
  - orchestration and event backbone
- Primary dependencies:
  - P01-T02
  - P01-T03
- Hands off to:
  - WS-03 for evidence processing
  - WS-06 for retrieval and analytics
  - WS-07 for BFF query paths

## WS-03 Ingestion And Evidence Processing

- Owner archetype:
  - document-processing lead
- Scope:
  - harvester
  - downloader
  - manifest
  - deduplication
  - routing
  - PDF processing
  - OCR and layout extraction
  - canonical document/page/span persistence
- Primary tasks:
  - P02-T01
  - P02-T02
  - P02-T03
  - P02-T04
  - P02-T06
  - P02-T07
- Main outputs:
  - immutable and replayable evidence layer
  - canonical evidence dataset
- Accountable artifacts:
  - ingest manifest
  - canonical `Document`, `Page`, and `Span`
  - page image/native/OCR linkage
- Hands off to:
  - WS-04 for sensitivity and review
  - WS-05 for semantic extraction
  - WS-07 for document-viewer reads

## WS-04 Policy, Security, And Review

- Owner archetype:
  - policy/security lead
- Scope:
  - sensitivity tagging
  - role model
  - OPA policy
  - datastore enforcement
  - export rules
  - adjudication flows
  - audit logging
- Primary tasks:
  - P03-T01
  - P03-T02
  - P03-T03
  - P03-T04
  - P03-T05
  - portions of P01-T07
- Main outputs:
  - safe access control path
  - review and adjudication substrate
- Accountable artifacts:
  - sensitivity annotations
  - policy decision model
  - review items and adjudications
  - audit events
- Hands off to:
  - every other workstream, because policy constrains promotion and access everywhere

## WS-05 Semantics, Extraction, And Resolution

- Owner archetype:
  - semantics lead
- Scope:
  - entity extraction
  - alias handling
  - identity resolution
  - thread reconstruction
  - relation extraction
  - event extraction
  - temporal normalization
  - redaction modeling
- Primary tasks:
  - P04-T01
  - P04-T02
  - P04-T03
  - P04-T04
  - P04-T05
  - P04-T06
- Main outputs:
  - structured, evidence-backed semantic layer
- Accountable artifacts:
  - entity candidates and canonical entities
  - relation records
  - event records
  - redaction objects
- Hands off to:
  - WS-06 for retrieval, graph, and analytics
  - WS-07 for dossiers and evidence views
  - WS-08 for QA

## WS-06 Retrieval, Graph, And Analytics

- Owner archetype:
  - retrieval/analytics lead
- Scope:
  - indexing
  - embeddings and rerank
  - graph materialization
  - event-based analytics
  - topic modeling
  - weak supervision
  - evaluation tracking
- Primary tasks:
  - P05-T01
  - P05-T02
  - P05-T03
  - P05-T04
  - P05-T05
  - P05-T06
- Main outputs:
  - analyst retrieval and analytical substrate
- Accountable artifacts:
  - retrieval artifacts and index mappings
  - graph projections
  - analytics tables
  - topic artifacts
  - weak-label outputs
- Hands off to:
  - WS-07 for search and analytics UI
  - WS-08 for QA and advanced analytical surfaces

## WS-07 BFF And Web Application

- Owner archetype:
  - application lead
- Scope:
  - FastAPI orchestration layer
  - Next.js shell
  - search
  - document viewer
  - entity and event views
  - review workbench
  - job-state UX
- Primary tasks:
  - P06-T01
  - P06-T02
  - P06-T03
  - P06-T04
  - P06-T05
  - P06-T06
  - P06-T07
- Accountable artifacts:
  - BFF response envelopes
  - route-level analyst experiences
  - document viewer and review workflows
- Hands off to:
  - WS-08 for QA-specific and advanced UX expansion

## WS-08 QA, Advanced UX, And Release Engineering

- Owner archetype:
  - release lead
  - application lead
- Scope:
  - controlled QA
  - citation UX
  - support verification
  - graph explorer and topic atlas UI
  - restricted redaction atlas
  - SLO dashboards
  - hardening and release readiness
- Primary tasks:
  - P07-T01
  - P07-T02
  - P07-T03
  - P07-T04
- Accountable artifacts:
  - QA evidence packs
  - QA answer artifacts
  - advanced analytical views
  - release-readiness package

## Ownership Guidance

- Assign owners by workstream first, then by phase.
- Treat the owner archetype as accountable for signoff evidence, even if implementation is delegated.
- Do not assign one subagent simultaneous ownership of two file-heavy tasks in the same code area.
- Use the work-package template in [`work-packages/TEMPLATE.md`](./work-packages/TEMPLATE.md) for all delegated implementation.
