# Phase 05 - Retrieval, Graph, Analytics, And Hypothesis Layer

Status: planned

## Objective

Build the retrieval, graph, analytics, topic, and weak-supervision layers on top of the evidence-backed semantic foundation.

## Architecture Traceability

- `Architecture_Plan.md` lines 197-243
- `Architecture_Plan.md` lines 245-253
- `Architecture_Plan.md` lines 365-403
- `Architecture_Plan.md` lines 438-446

## Entry Criteria

- structured semantics dataset exists
- policy enforcement exists for derived artifacts

## Exit Criteria

- hybrid retrieval works
- graph materialization works
- event-based analytics tables exist
- topic and weak-supervision lanes exist with evaluation hooks
- expanded validation and MLflow tracking exist

## Phase Handoff Summary

- Consumes:
  - A-018 through A-021
  - A-011 through A-015 where policy or review affects promotion
- Produces:
  - A-022 through A-027
  - search, graph, analytics, and evaluation substrates for the application layer
- Blocking open questions:
  - OQ-05 gold-set curation ownership
  - OQ-02 budget and capacity envelope for large-scale embedding and model work
- Primary workstreams:
  - WS-06 Retrieval, Graph, And Analytics
- Primary signoff roles:
  - retrieval/analytics lead
  - semantics lead for model-assisted analytical lanes
  - policy/security lead where restricted surfaces are involved
- Earliest safe parallel starts:
  - Phase 06 can begin once stable read contracts and minimum retrieval services exist
  - Phase 07 QA prototyping can begin once evidence-pack inputs are stable

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P05-T01 | planned | P04-T06, P03-T03 |
| P05-T02 | planned | P04-T06, P03-T03 |
| P05-T03 | planned | P04-T04, P01-T04 |
| P05-T04 | planned | P04-T06 |
| P05-T05 | planned | P04-T06, P03-T04 |
| P05-T06 | planned | P05-T01, P05-T03 |

## P05-T01 Build Retrieval Indexing, Embeddings, And Rerank Pipeline

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-10, AC-16, AC-18
- Objective: provide explainable hybrid retrieval over the correct artifact classes.
- Dependencies: blocking on P04-T06 and P03-T03
- Parallelization: parallelizable with P05-T02 and P05-T03
- Required external decisions: OQ-05 for evaluation ownership
- Deliverables:
  - artifact indexing model
  - embedding pipeline
  - hybrid search pipeline
  - rerank path
- Acceptance criteria:
  - artifact classes are explicit
  - restricted content is filtered appropriately
  - search can explain lexical, semantic, and graph-expansion reasons
- Subtasks:
  1. `P05-T01-S01` Define the retrieval artifact schema set and index mappings.
     Depends on: P04-T06-S04, P03-T03-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T02-S01
     Concrete output: retrieval schema set
  2. `P05-T01-S02` Implement embedding generation for the required artifact classes.
     Depends on: P05-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T01-S03
     Concrete output: embedding pipeline
  3. `P05-T01-S03` Implement OpenSearch lexical-plus-vector indexing and metadata filters.
     Depends on: P05-T01-S01, P03-T03-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T01-S02
     Concrete output: hybrid index pipeline
  4. `P05-T01-S04` Implement second-stage reranking and search-explanation payloads.
     Depends on: P05-T01-S02, P05-T01-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S01 later
     Concrete output: rerank and explanation layer

## P05-T02 Build Graph Schema Materialization And Graph-Service Queries

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-11, AC-16, AC-18
- Objective: materialize the canonical graph from evidence-backed semantics and provide bounded query surfaces.
- Dependencies: blocking on P04-T06 and P03-T03
- Parallelization: parallelizable with P05-T01 and P05-T03
- Required external decisions: none
- Deliverables:
  - graph schema implementation
  - projection builder
  - bounded graph query surfaces
- Acceptance criteria:
  - graph nodes and edges follow the canonical schema
  - evidence-backed and inferred edges are distinguishable
  - bounded subgraph queries support later UI work
- Subtasks:
  1. `P05-T02-S01` Map structured semantics into graph node and edge classes.
     Depends on: P04-T06-S04, P04-T02-S04, P04-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T01-S01
     Concrete output: graph mapping spec
  2. `P05-T02-S02` Implement graph materialization and rematerialization flow.
     Depends on: P05-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T02-S03
     Concrete output: graph builder
  3. `P05-T02-S03` Implement bounded subgraph query patterns and policy-aware graph service helpers.
     Depends on: P05-T02-S01, P03-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T02-S02
     Concrete output: graph-service query layer
  4. `P05-T02-S04` Validate graph edge classes, query bounds, and traceability to evidence.
     Depends on: P05-T02-S02, P05-T02-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: graph validation report

## P05-T03 Build Event-Based Analytics Tables And Dashboard Backend

- Status: planned
- Relevant constraints: AC-03, AC-11, AC-16, AC-18
- Objective: create analytical tables and backend query surfaces for time-series and saved analytics.
- Dependencies: blocking on P04-T04 and P01-T04
- Parallelization: parallelizable with P05-T01 and P05-T02
- Required external decisions: none
- Deliverables:
  - event-based derived tables
  - analytics query surfaces
  - uncertainty-ready contracts
- Acceptance criteria:
  - analytics derive from event-centric structures
  - saved analytics do not overload the search index
  - time uncertainty is preserved in outputs
- Subtasks:
  1. `P05-T03-S01` Define derived-table contracts for activity, lag, and co-occurrence analytics.
     Depends on: P04-T04-S04, P01-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T01-S01
     Concrete output: analytics table spec
  2. `P05-T03-S02` Implement batch or streaming materialization of derived analytics tables.
     Depends on: P05-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T03-S03
     Concrete output: analytics materialization pipeline
  3. `P05-T03-S03` Implement backend query helpers or endpoints for analytics consumers.
     Depends on: P05-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T03-S02
     Concrete output: analytics backend surface
  4. `P05-T03-S04` Validate uncertainty handling and query performance on representative views.
     Depends on: P05-T03-S02, P05-T03-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: analytics validation report

## P05-T04 Build Topic Modeling And Sense-Induction Research Lane

- Status: planned
- Relevant constraints: AC-03, AC-16, AC-18
- Objective: build topic and sense-induction capabilities as explicitly derived and reviewable hypothesis layers.
- Dependencies: soft_dependency on P04-T06
- Parallelization: parallelizable with P05-T01, P05-T03, and P05-T05
- Required external decisions: OQ-05
- Deliverables:
  - topic pipeline by document family
  - temporal topic tracking
  - sense-induction research lane
- Acceptance criteria:
  - topic outputs remain derived and reviewable
  - document-family segmentation is explicit
  - unstable outputs are not promoted as fact
- Subtasks:
  1. `P05-T04-S01` Segment the corpus by document family for topic workflows.
     Depends on: P04-T06-S02
     Dependency classification: soft_dependency
     Parallelization: parallelizable with P05-T01-S02
     Concrete output: family segmentation inputs
  2. `P05-T04-S02` Implement per-family topic modeling and topic-over-time materialization.
     Depends on: P05-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T04-S03
     Concrete output: topic pipeline
  3. `P05-T04-S03` Implement sense-induction workflow for candidate coded-language clusters.
     Depends on: P05-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T04-S02
     Concrete output: sense-induction lane
  4. `P05-T04-S04` Define review and stability criteria before any topic output is promoted.
     Depends on: P05-T04-S02, P05-T04-S03, P03-T04-S01
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: topic promotion criteria

## P05-T05 Build Weak Supervision And Calibration Lane

- Status: planned
- Relevant constraints: AC-06, AC-07, AC-08, AC-16, AC-17
- Objective: build the weak-supervision and LLM-judge layer without turning it into an evidentiary authority.
- Dependencies: soft_dependency on P04-T06 and blocking on P03-T04
- Parallelization: parallelizable with P05-T04
- Required external decisions: OQ-05
- Deliverables:
  - label set
  - labeling-function baseline
  - probabilistic label model
  - calibration workflow
- Acceptance criteria:
  - labels remain non-accusatory and attached to spans, events, or clusters
  - disagreement is surfaced as uncertainty
  - calibrated thresholds exist before promotion
- Subtasks:
  1. `P05-T05-S01` Define the label taxonomy and promotion boundaries for weak signals.
     Depends on: P03-T04-S01, P04-T06-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T04-S01
     Concrete output: weak-label taxonomy
  2. `P05-T05-S02` Implement deterministic, classifier-based, and LLM-judge labeling functions.
     Depends on: P05-T05-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T05-S03
     Concrete output: labeling-function set
  3. `P05-T05-S03` Implement label-model aggregation and telemetry capture.
     Depends on: P05-T05-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T04-S02
     Concrete output: probabilistic label model
  4. `P05-T05-S04` Calibrate thresholds against reviewed data and define promotion rules.
     Depends on: P05-T05-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: calibration report

## P05-T06 Expand MLflow, Evaluation, And Data-Quality Checkpoints

- Status: planned
- Relevant constraints: AC-17, AC-18
- Objective: track experiments, evaluations, and quality regressions across core analytical components.
- Dependencies: blocking on P05-T01 and P05-T03
- Parallelization: parallelizable with later portions of P05-T04 and P05-T05
- Required external decisions: OQ-05
- Deliverables:
  - experiment-tracking baseline
  - evaluation dataset registry
  - regression suites and thresholds
- Acceptance criteria:
  - major model-assisted workflows have evaluation hooks
  - thresholds are versioned and reviewable
  - release gates can depend on observed metrics
- Subtasks:
  1. `P05-T06-S01` Implement MLflow tracking for OCR, extraction, retrieval, topic, and QA-adjacent experiments.
     Depends on: P05-T01-S04, P05-T03-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T06-S02
     Concrete output: experiment tracking baseline
  2. `P05-T06-S02` Define evaluation datasets, dataset lineage, and result storage conventions.
     Depends on: P05-T06-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T06-S03
     Concrete output: evaluation registry
  3. `P05-T06-S03` Implement regression suites and threshold checks for core analytical workflows.
     Depends on: P05-T06-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T04-S01 later
     Concrete output: analytical regression suite
  4. `P05-T06-S04` Publish quality baselines and threshold review procedures.
     Depends on: P05-T06-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: analytical quality baseline
