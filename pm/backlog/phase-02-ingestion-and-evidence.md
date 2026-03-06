# Phase 02 - Immutable Ingestion And Canonical Evidence Layer

Status: planned

## Objective

Acquire lawful source data, preserve it immutably, process it deterministically, and materialize the canonical evidence layer required for every downstream feature.

## Architecture Traceability

- `Architecture_Plan.md` lines 97-129
- `Architecture_Plan.md` lines 131-163
- `Architecture_Plan.md` lines 263-289

## Entry Criteria

- core stateful services and orchestration baseline exist
- canonical schema and provenance contracts are defined

## Exit Criteria

- lawful source discovery is incremental and auditable
- raw evidence is versioned and replayable
- routing, docproc, OCR, and page/span materialization are operational
- validation and lineage are available on evidence assets

## Phase Handoff Summary

- Consumes:
  - Phase 01 platform substrate
  - Phase 00 schema and provenance contracts
- Produces:
  - A-001 through A-010 from [`../14_artifact_inventory.md`](../14_artifact_inventory.md)
  - accepted evidence-layer cohort for downstream work
- Blocking open questions:
  - OQ-01 deployment environment
  - OQ-02 budget and capacity envelope
  - OQ-05 gold-set curation ownership
- Primary workstreams:
  - WS-02 Data Plane And Orchestration
  - WS-03 Ingestion And Evidence Processing
- Primary signoff roles:
  - data plane lead
  - document-processing lead
- Earliest safe parallel starts:
  - Phase 03 may begin on accepted evidence assets
  - Phase 04 may prototype only on accepted evidence cohorts

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P02-T01 | planned | P01-T04, P01-T05 |
| P02-T02 | planned | P02-T01, P00-T02 |
| P02-T03 | planned | P02-T02 |
| P02-T04 | planned | P02-T03, P00-T02 |
| P02-T05 | planned | P02-T04 |
| P02-T06 | planned | P02-T01, P02-T03 |
| P02-T07 | planned | P02-T04, P02-T05 |

## P02-T01 Build Harvester, Downloader, And Ingest-Branch Workflow

- Status: planned
- Relevant constraints: AC-01, AC-04, AC-13
- Objective: discover and fetch official source material into immutable, branch-scoped raw storage.
- Dependencies: blocking on P01-T04 and P01-T05
- Parallelization: parallelizable with P02-T02 after raw ingest events exist
- Required external decisions: OQ-01 if environment-specific storage configuration is unresolved
- Deliverables:
  - harvester service
  - downloader service
  - ingest batch/branch workflow
- Acceptance criteria:
  - official source URLs can be discovered and re-discovered
  - downloads are hashed and stored immutably
  - every ingest batch has an auditable lakeFS branch
- Subtasks:
  1. `P02-T01-S01` Define the official-source seed list and discovery rules.
     Depends on: P01-T04-S04
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: seed configuration
  2. `P02-T01-S02` Implement downloader behavior that records response headers, MIME, length, and SHA-256.
     Depends on: P02-T01-S01, P00-T02-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T01-S03
     Concrete output: downloader implementation
  3. `P02-T01-S03` Implement lakeFS ingest-branch creation, merge, and audit-retention logic.
     Depends on: P01-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T01-S02
     Concrete output: ingest-branch workflow
  4. `P02-T01-S04` Emit manifest-ready ingest events for downstream consumers.
     Depends on: P02-T01-S02, P02-T01-S03, P01-T05-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T02-S01
     Concrete output: ingest event emission

## P02-T02 Build Manifest, Deduplication, And Routing Services

- Status: planned
- Relevant constraints: AC-04, AC-13, AC-18
- Objective: create auditable manifest records, duplicate-group logic, and deterministic content routing.
- Dependencies: blocking on P02-T01 and P00-T02
- Parallelization: parallelizable with P02-T03 after routing contract is stable
- Required external decisions: none
- Deliverables:
  - ingest manifest asset
  - duplicate-set model
  - MIME and magic-byte router
- Acceptance criteria:
  - manifest records carry required provenance
  - exact and near duplicates are grouped without deletion
  - routing is deterministic and logged
- Subtasks:
  1. `P02-T02-S01` Materialize the manifest asset in PostgreSQL and Iceberg.
     Depends on: P02-T01-S04, P00-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T02-S02
     Concrete output: manifest pipeline
  2. `P02-T02-S02` Implement exact-duplicate and near-duplicate grouping rules.
     Depends on: P02-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T02-S03
     Concrete output: duplicate-group pipeline
  3. `P02-T02-S03` Implement deterministic content routing based on MIME and magic bytes.
     Depends on: P02-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T02-S02
     Concrete output: routing service
  4. `P02-T02-S04` Validate manifest completeness and routing determinism.
     Depends on: P02-T02-S02, P02-T02-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: routing validation record

## P02-T03 Build PDF, Layout, And OCR Processing Lanes

- Status: planned
- Relevant constraints: AC-14, AC-17, AC-18
- Objective: process documents through structural parsing, layout extraction, and tiered OCR recovery.
- Dependencies: blocking on P02-T02
- Parallelization: parallelizable with P02-T04
- Required external decisions: OQ-02, OQ-05
- Deliverables:
  - PDF processing lane
  - layout extraction lane
  - OCR fallback lane
- Acceptance criteria:
  - native extraction, geometric extraction, and OCR fallbacks are explicit
  - confidence thresholds are recorded
  - image/native/OCR layers can be preserved downstream
- Subtasks:
  1. `P02-T03-S01` Implement structural PDF parsing and attachment handling.
     Depends on: P02-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T03-S02
     Concrete output: structural parse lane
  2. `P02-T03-S02` Implement geometric extraction and layout partitioning.
     Depends on: P02-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T03-S01
     Concrete output: layout lane
  3. `P02-T03-S03` Implement tiered OCR routing and fallback handling.
     Depends on: P02-T03-S01, P02-T03-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: OCR lane
  4. `P02-T03-S04` Build threshold calibration harness and difficult-page review feed.
     Depends on: P02-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T04-S01 later
     Concrete output: OCR calibration harness

## P02-T04 Materialize Canonical Document, Page, And Span Assets

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-14, AC-16
- Objective: persist the canonical evidence layer so downstream systems have stable, provenance-rich evidence objects.
- Dependencies: blocking on P02-T03 and P00-T02
- Parallelization: parallelizable with P02-T05
- Required external decisions: none
- Deliverables:
  - `Document`, `Page`, and `Span` assets
  - extractor identity recording
  - evidence read APIs or access helpers
- Acceptance criteria:
  - evidence objects are materialized in the planned stores
  - extractor identity is preserved
  - page image/native/OCR linkage is retained
- Subtasks:
  1. `P02-T04-S01` Map parser and OCR outputs into canonical document/page/span structures.
     Depends on: P02-T03-S03, P00-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T04-S02
     Concrete output: canonicalization mapper
  2. `P02-T04-S02` Persist canonical assets into Iceberg and operational lookup stores.
     Depends on: P02-T04-S01, P01-T04-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T05-S01
     Concrete output: evidence persistence
  3. `P02-T04-S03` Persist page image/native/OCR relationships and extraction-engine identity.
     Depends on: P02-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T04-S02
     Concrete output: evidence-layer linkage
  4. `P02-T04-S04` Validate canonical asset completeness and source-to-span traceability.
     Depends on: P02-T04-S02, P02-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: canonical evidence validation

## P02-T05 Implement Lineage, Validation, And Replay Controls

- Status: planned
- Relevant constraints: AC-04, AC-13, AC-16, AC-17
- Objective: ensure evidence assets are validated, traceable, and replayable from known ingest states.
- Dependencies: blocking on P02-T04
- Parallelization: parallelizable with P02-T06
- Required external decisions: none
- Deliverables:
  - data validation checkpoints
  - lineage metadata path
  - replay and rematerialization controls
- Acceptance criteria:
  - evidence-layer checkpoints exist
  - lineage across lakeFS, Dagster, and Iceberg can be traversed
  - failure branches are auditable
- Subtasks:
  1. `P02-T05-S01` Define validation checkpoints for manifest, page counts, required provenance, and schema conformance.
     Depends on: P02-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T06-S01
     Concrete output: evidence validation suite
  2. `P02-T05-S02` Wire lineage metadata across ingest branch, asset materialization, and evidence records.
     Depends on: P02-T04-S02, P01-T05-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T05-S01
     Concrete output: lineage integration
  3. `P02-T05-S03` Define replay and rematerialization procedures for evidence assets.
     Depends on: P02-T05-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: replay procedure
  4. `P02-T05-S04` Validate replayability on a controlled ingest sample.
     Depends on: P02-T05-S01, P02-T05-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: replay validation record

## P02-T06 Build Ingest Observability And Failure Handling

- Status: planned
- Relevant constraints: AC-17
- Objective: make ingest and docproc failures visible, measurable, and recoverable.
- Dependencies: blocking on P02-T01 and P02-T03
- Parallelization: parallelizable with P02-T05
- Required external decisions: none
- Deliverables:
  - ingest metrics
  - queue-depth and failure dashboards
  - retry and quarantine rules
- Acceptance criteria:
  - major failure classes are observable
  - retry behavior is bounded and auditable
  - quarantine path exists for bad or incomplete inputs
- Subtasks:
  1. `P02-T06-S01` Define operational metrics for harvest, download, parse, OCR, and materialization stages.
     Depends on: P02-T01-S04, P02-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T05-S01
     Concrete output: ingest metric spec
  2. `P02-T06-S02` Implement dashboards and alerts for queue depth, lag, and failure rates.
     Depends on: P02-T06-S01, P01-T06-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T06-S03
     Concrete output: ingest dashboards
  3. `P02-T06-S03` Define retry, quarantine, and operator-intervention paths.
     Depends on: P02-T03-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T06-S02
     Concrete output: failure-handling runbook
  4. `P02-T06-S04` Test representative failure and recovery scenarios.
     Depends on: P02-T06-S02, P02-T06-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: recovery validation record

## P02-T07 Produce Evidence-Layer MVP Dataset And Acceptance Checks

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-14, AC-17
- Objective: assemble the first accepted evidence-layer dataset that downstream phases can safely consume.
- Dependencies: blocking on P02-T04 and P02-T05
- Parallelization: none
- Required external decisions: OQ-05 if gold-set review ownership is unresolved
- Deliverables:
  - accepted evidence-layer sample or cohort
  - acceptance report
  - downstream-readiness signoff
- Acceptance criteria:
  - evidence assets pass validation
  - representative documents show usable image/native/OCR reconciliation
  - downstream consumers can read the canonical layer
- Subtasks:
  1. `P02-T07-S01` Select the initial representative ingest cohort.
     Depends on: P02-T05-S04
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: MVP cohort definition
  2. `P02-T07-S02` Run end-to-end ingest, docproc, and canonicalization on the cohort.
     Depends on: P02-T07-S01
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: evidence-layer dataset
  3. `P02-T07-S03` Validate the cohort against evidence quality and provenance gates.
     Depends on: P02-T07-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: acceptance report
  4. `P02-T07-S04` Publish downstream consumption guidance for Phase 03 and Phase 04.
     Depends on: P02-T07-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: downstream-readiness note
