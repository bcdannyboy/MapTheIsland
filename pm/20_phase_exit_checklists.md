# Phase Exit Checklists

These checklists define what must be true before a phase is considered complete enough to hand off to dependent work.

## Global Exit Prerequisites

- local automated tests for the phase scope pass at 100 percent
- integration tests for the phase scope pass at 100 percent
- handwritten code for the phase scope remains at 100 percent coverage
- required documentation, docstrings, and operational notes are present for newly introduced code and workflows

## Phase 00 Exit

- implementation spec exists
- architecture-to-task traceability exists
- canonical schema baseline exists
- policy taxonomy baseline exists
- service boundary baseline exists
- engineering standard baseline exists
- testing, coverage, and documentation enforcement rules are explicit and toolable
- unresolved external decisions are visible, not hidden
- PM workspace is internally consistent

## Phase 01 Exit

- monorepo structure exists
- infrastructure is provisionable from code
- GitOps baseline exists
- secrets and certificate flow exist
- core stateful services are reachable
- Dagster and event baseline exist
- CI and observability baseline exist
- auth foundation exists

## Phase 02 Exit

- lawful-source harvesting is incremental and auditable
- raw evidence is immutable and branch-versioned
- manifest, deduplication, and routing work
- image, native, and OCR layers can be preserved
- canonical evidence assets exist with provenance
- evidence validation exists
- replay or rematerialization path exists
- ingest metrics and failure handling exist

## Phase 03 Exit

- sensitivity tagging runs before broad promotion
- policy engine can evaluate representative decisions
- datastore-level enforcement exists where planned
- review queues and adjudication APIs work
- export-control logic exists
- audit events exist for sensitive actions
- policy-denied actions and review metrics are observable

## Phase 04 Exit

- entity and alias extraction work
- identity resolution creates reviewable merge candidates
- thread reconstruction records fragmentary cases
- relation extraction is schema-validated
- event extraction and temporal normalization exist
- redaction objects exist with safe handling
- structured semantics dataset is published for downstream consumers

## Phase 05 Exit

- retrieval artifact classes are defined and indexed
- hybrid retrieval works with policy filtering
- graph materialization distinguishes evidence classes
- event-based analytics tables exist
- topic and weak-supervision lanes have promotion controls
- evaluation and MLflow coverage exist for major workflows

## Phase 06 Exit

- BFF mediates browser access
- application shell exists
- search works
- document viewer exposes image, native, and OCR layers
- entity and event routes work
- review workbench works
- long-running jobs expose deterministic status
- evidence workbench MVP acceptance report exists

## Phase 07 Exit

- QA uses evidence packs
- support verification and abstention work
- citations deep-link to evidence
- advanced analytics obey policy boundaries
- full regression and evaluation evidence exists
- SLO dashboards and runbooks exist
- backup, recovery, and rollback are validated
- release-readiness package exists

## Required Handoff Updates

At each phase exit, update:

- the completed phase backlog file
- [`11_status_dashboard.md`](./11_status_dashboard.md)
- [`06_risk_register.md`](./06_risk_register.md)
- [`07_decision_log.md`](./07_decision_log.md) if a durable decision was made
- [`08_research_register.md`](./08_research_register.md) if new sources were used
- the current session log
