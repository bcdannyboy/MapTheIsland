# Program Charter

## Purpose

MapTheIsland is being planned as a provenance-first analytical platform over the public DOJ Epstein corpus. The platform is intended to ingest lawful source material, preserve immutable evidence, derive structured analytical assets without severing provenance, protect victim-sensitive context, and provide an evidence workbench for analysts that includes search, document inspection, structured dossiers, timelines, graph analysis, review queues, and controlled question answering.

## Source Basis

This charter is based on the reference architecture in [`Architecture_Plan.md`](../Architecture_Plan.md). It is also supported by current official documentation reviewed on 2026-03-06 and cataloged in [`08_research_register.md`](./08_research_register.md). The planning baseline does not assume undocumented product scope beyond what the architecture states.

## Problem Statement

The source corpus is large, updateable, multimodal, partially hard to search, and subject to victim-protective redaction constraints. A conventional “chat over PDFs” workflow would fail on provenance, policy control, replayability, and evidentiary inspection. The program therefore must deliver:

- immutable source acquisition and replayable ingest
- span-level canonical evidence objects with provenance
- policy-sensitive extraction and review infrastructure
- evidence-backed semantic layers for entities, events, topics, and graph analysis
- a policy-filtered UI that exposes evidence rather than opaque model output
- a controlled QA experience that abstains when support is weak or policy blocks disclosure

## Included Scope

The planned program includes all major capabilities named in the architecture:

- self-managed platform control plane and GitOps delivery model
- S3-compatible evidence storage with lakeFS versioning
- Iceberg analytical assets and Trino analytical SQL surface
- PostgreSQL operational metadata and adjudication storage
- OpenSearch retrieval and hybrid search
- Neo4j graph representation and graph analytics
- Dagster orchestration and Kafka event backbone
- OCR, PDF parsing, layout extraction, canonical page/span generation
- sensitivity tagging, redaction-safe handling, and policy enforcement
- entity extraction, aliasing, identity resolution, thread reconstruction, relation extraction, and event extraction
- topic modeling, weak supervision, temporal analytics, and retrieval artifact generation
- FastAPI BFF and Next.js evidence workbench UI
- review workbench, evaluation infrastructure, observability, release controls, and launch hardening

## Explicit Non-Goals

The following are out of scope because the architecture explicitly rejects them:

- deanonymization of redactions or inferred victim identities
- person-level risk scoring or accusation generation
- a single-store architecture that collapses evidence, operations, search, graph, and analytics into one system
- a browser that talks directly to privileged datastores or model providers
- a generic chatbot shipped ahead of evidence visibility, policy enforcement, and support verification

## Program Outcomes

The program is complete only when all of the following are true:

- every derived analytical object can be traced back to raw evidence and versioned processing lineage
- victim-protective policy controls are enforced in ingest, extraction, storage, retrieval, export, and QA workflows
- analysts can inspect documents through image, native text, and OCR layers without ambiguity about extraction mode
- entities, events, topics, graph neighborhoods, and timelines are grounded in supporting spans and explicit confidence states
- low-confidence, sensitive, or high-impact outputs are reviewable and adjudicable through a dedicated workflow
- QA outputs carry citations, support classification, and abstention behavior
- release readiness is demonstrated through validation, evaluation, access control, observability, and rollback procedures

## Measurable Success Criteria

### Evidence And Provenance

- 100 percent of `Document`, `Page`, `Span`, `Claim`, retrieval artifact, and QA citation objects include the required provenance fields.
- Raw evidence is immutable in storage and replayable by ingest batch and branch.
- Every analyst-visible fact can deep-link back to a source document, page, and highlighted span.

### Policy And Safety

- Restricted spans are excluded from broad search indices and unauthorized QA prompts.
- High-impact entity merges, sensitive labels, and policy-sensitive exports require human adjudication.
- Redaction-neighbor context is masked or hashed where required by policy.

### Product Usability

- Search, document viewer, entity dossier, event explorer, review workbench, and timeline views are usable without direct datastore access from the browser.
- Long-running jobs expose observable status and deterministic completion states.
- Saved views, filters, and bookmarked URLs reproduce the same result set subject to role filtering and asset versioning.

### Engineering Readiness

- Infrastructure is reproducible from code.
- Contracts, schemas, and tests are versioned and enforced in CI.
- Evaluation gates exist for OCR, extraction, retrieval, support verification, and policy enforcement.
- SLO dashboards and release criteria exist before pilot rollout.

## Delivery Boundary For The First Credible Release

The first credible release is the evidence workbench, consisting of:

- immutable ingest
- canonical document/page/span assets
- sensitivity enforcement
- basic entity and event extraction
- hybrid search
- document viewer with image/native/OCR toggles
- entity and event pages
- review workbench
- lineage and audit visibility

Controlled QA, graph explorer expansion, topic atlas, redaction atlas, and richer analytics are later release milestones, not first-release prerequisites.

## Required External Decisions

The following decisions are required before implementation can move from plan to execution. They are not assumed in this workspace:

- deployment environment selection: AWS, on-premises, or another self-managed environment compatible with the architecture
- domain, DNS, and certificate ownership model for deployed environments
- budget envelope for GPU capacity, object storage growth, and stateful infrastructure
- staffing or agent-allocation model across infra, data engineering, ML/NLP, backend, frontend, security/policy, and QA
- legal or policy signoff path for restricted-role definitions and export controls
- release audience for internal alpha, analyst preview, and restricted pilot

These open items are tracked in [`research/open-questions.md`](./research/open-questions.md).

## References

- [`Architecture_Plan.md`](../Architecture_Plan.md): lines 1-20, 60-109, 131-171, 205-257, 263-289, 293-468
- [`08_research_register.md`](./08_research_register.md)
