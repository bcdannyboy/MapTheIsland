# Phase 04 - Structured Extraction And Evidence-Backed Semantics

Status: planned

## Objective

Transform canonical spans into evidence-backed semantic objects: entities, aliases, relations, threads, events, and redaction objects.

## Architecture Traceability

- `Architecture_Plan.md` lines 173-195
- `Architecture_Plan.md` lines 205-213
- `Architecture_Plan.md` lines 225-231

## Entry Criteria

- evidence-layer MVP dataset exists
- sensitivity and review infrastructure exists

## Exit Criteria

- entity and alias extraction operational
- merge-review-safe identity resolution operational
- relation and event extraction operational
- redaction objects operational
- structured semantics dataset available downstream

## Phase Handoff Summary

- Consumes:
  - A-007 through A-010
  - A-011 through A-014
- Produces:
  - A-016 through A-021
  - accepted structured semantics cohort for retrieval, graph, analytics, and UI work
- Blocking open questions:
  - OQ-05 gold-set curation ownership
  - OQ-03 for redaction and merge-review governance details
- Primary workstreams:
  - WS-05 Semantics, Extraction, And Resolution
  - WS-04 Policy, Security, And Review for review coupling
- Primary signoff roles:
  - semantics lead
  - policy/security lead for redaction safety and review-sensitive promotion
- Earliest safe parallel starts:
  - Phase 05 research lanes may begin on pilot semantic outputs
  - Phase 06 dossier prototyping may begin against stable semantic contracts

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P04-T01 | planned | P02-T07, P03-T01 |
| P04-T02 | planned | P04-T01, P03-T04 |
| P04-T03 | planned | P02-T07, P03-T01 |
| P04-T04 | planned | P04-T01, P04-T03 |
| P04-T05 | planned | P02-T07, P03-T01 |
| P04-T06 | planned | P04-T02, P04-T04, P04-T05 |

## P04-T01 Build Entity And Alias Extraction Pipeline

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-07, AC-10, AC-18
- Objective: extract deterministic and learned entity candidates plus alias candidates anchored to source spans.
- Dependencies: blocking on P02-T07 and P03-T01
- Parallelization: parallelizable with P04-T03
- Required external decisions: OQ-05 if evaluation ownership is unresolved
- Deliverables:
  - entity candidate pipeline
  - alias candidate pipeline
  - evidence-linked candidate records
- Acceptance criteria:
  - entity candidates attach to source spans
  - deterministic and learned extraction paths are distinguishable
  - alias candidates remain non-canonical until resolution
- Subtasks:
  1. `P04-T01-S01` Implement deterministic extraction for structured identifiers and contact points.
     Depends on: P02-T07-S04, P03-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T01-S02
     Concrete output: deterministic entity lane
  2. `P04-T01-S02` Implement learned NER pipelines for people, organizations, locations, roles, and named objects.
     Depends on: P02-T07-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T01-S01
     Concrete output: learned entity lane
  3. `P04-T01-S03` Implement alias-cue mining for `aka`, quoted nicknames, email local parts, and signature patterns.
     Depends on: P04-T01-S01, P04-T01-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: alias-candidate lane
  4. `P04-T01-S04` Validate evidence linkage, confidence fields, and review-state handling for all candidate types.
     Depends on: P04-T01-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T03-S03
     Concrete output: extraction validation record

## P04-T02 Build Identity Resolution And Merge-Review Workflow

- Status: planned
- Relevant constraints: AC-04, AC-07, AC-16, AC-18
- Objective: resolve entity candidates into canonical identities without losing reviewability or evidence traceability.
- Dependencies: blocking on P04-T01 and P03-T04
- Parallelization: parallelizable with P04-T03 and early P05-T04 research work
- Required external decisions: OQ-05
- Deliverables:
  - blocking rules
  - pairwise scoring path
  - clustering path
  - merge-review workflow
- Acceptance criteria:
  - unreviewed merges are distinguishable from accepted canonical identity
  - merge inputs and outputs remain evidence-backed
  - merge-review tasks can be created and adjudicated
- Subtasks:
  1. `P04-T02-S01` Define blocking rules based on names, contact points, domains, roles, and thread co-occurrence.
     Depends on: P04-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T02-S02
     Concrete output: candidate-pair generation rules
  2. `P04-T02-S02` Implement pairwise scoring features and similarity pipeline.
     Depends on: P04-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T02-S01
     Concrete output: pairwise scorer
  3. `P04-T02-S03` Implement clustering and candidate-merge generation with review hooks.
     Depends on: P04-T02-S01, P04-T02-S02, P03-T04-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: merge-candidate pipeline
  4. `P04-T02-S04` Validate merge-review flow, rollback path, and downstream rematerialization trigger.
     Depends on: P04-T02-S03, P03-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P05-T02-S01 later
     Concrete output: identity-resolution validation report

## P04-T03 Build Thread Reconstruction And Relation Extraction

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-14, AC-18
- Objective: reconstruct document-specific threads and emit typed, schema-valid relations grounded in source spans.
- Dependencies: blocking on P02-T07 and P03-T01
- Parallelization: parallelizable with P04-T01 and P04-T05
- Required external decisions: none
- Deliverables:
  - thread reconstruction lane
  - relation schema and validators
  - relation extraction lane
- Acceptance criteria:
  - fragmentary rendering is recorded where needed
  - relations are schema-constrained and source-linked
  - relation validation rejects malformed outputs
- Subtasks:
  1. `P04-T03-S01` Implement email-header and quote-block parsing with subject normalization.
     Depends on: P02-T07-S04, P03-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T01-S01
     Concrete output: thread parse lane
  2. `P04-T03-S02` Add fragmentary-rendering detection and confidence scoring for imperfect email renderings.
     Depends on: P04-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T03-S03
     Concrete output: thread-confidence logic
  3. `P04-T03-S03` Define typed relation schemas and implement extraction with post-validators.
     Depends on: P04-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T03-S02
     Concrete output: relation extraction lane
  4. `P04-T03-S04` Validate thread grouping and relation correctness on representative samples.
     Depends on: P04-T03-S02, P04-T03-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: thread/relation validation report

## P04-T04 Build Event Extraction, Temporal Normalization, And Event Coreference

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-11, AC-18
- Objective: create the event-centric backbone required for graph, timeline, and QA workflows.
- Dependencies: blocking on P04-T01 and P04-T03
- Parallelization: parallelizable with P04-T05
- Required external decisions: OQ-05
- Deliverables:
  - event ontology implementation
  - event extraction pipeline
  - temporal normalization logic
  - cross-document event coreference
- Acceptance criteria:
  - events carry participants, time interval, location, evidence, and confidence
  - temporal uncertainty is explicit
  - multiple mentions can be resolved into one canonical event when justified
- Subtasks:
  1. `P04-T04-S01` Finalize the event ontology and schema validation rules.
     Depends on: P04-T01-S04, P04-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T04-S02
     Concrete output: event schema baseline
  2. `P04-T04-S02` Implement event extraction against the canonical span and relation outputs.
     Depends on: P04-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T04-S03
     Concrete output: event extraction lane
  3. `P04-T04-S03` Implement conservative temporal normalization and interval recording.
     Depends on: P04-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T04-S02
     Concrete output: temporal normalization lane
  4. `P04-T04-S04` Implement cross-document event coreference and validate event-centric downstream readiness.
     Depends on: P04-T04-S02, P04-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: event-coreference validation report

## P04-T05 Build Redaction Object Modeling And Safe Analytical Handling

- Status: planned
- Relevant constraints: AC-02, AC-10, AC-12
- Objective: model redactions as first-class analytical objects without creating deanonymization pathways.
- Dependencies: blocking on P02-T07 and P03-T01
- Parallelization: parallelizable with P04-T03 and P04-T04
- Required external decisions: OQ-03
- Deliverables:
  - redaction object schema
  - safe-neighborhood handling rules
  - redaction analysis baseline
- Acceptance criteria:
  - redactions are explicitly modeled
  - local context handling obeys masking or hashing rules
  - redaction analytics remain policy-safe
- Subtasks:
  1. `P04-T05-S01` Define the `Redaction` object schema and evidence attachment model.
     Depends on: P02-T07-S04, P03-T01-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T03-S01
     Concrete output: redaction schema
  2. `P04-T05-S02` Implement detection and recording of redaction geometry, signatures, and length classes.
     Depends on: P04-T05-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T05-S03
     Concrete output: redaction detection lane
  3. `P04-T05-S03` Implement masked or hashed neighborhood handling and restricted export safeguards.
     Depends on: P04-T05-S01, P03-T03-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P04-T05-S02
     Concrete output: safe redaction-handling logic
  4. `P04-T05-S04` Validate that redaction analytics do not expose prohibited adjacency context.
     Depends on: P04-T05-S02, P04-T05-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: redaction-safety validation report

## P04-T06 Deliver Structured Semantics MVP Dataset

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-11, AC-16
- Objective: publish the first accepted dataset of entities, relations, events, and redactions for downstream systems.
- Dependencies: blocking on P04-T02, P04-T04, and P04-T05
- Parallelization: none
- Required external decisions: OQ-05
- Deliverables:
  - accepted structured semantics dataset
  - downstream contract guidance
  - acceptance report
- Acceptance criteria:
  - semantic objects are evidence-backed and review-aware
  - downstream retrieval, graph, and UI consumers can read the dataset
  - known limitations are documented
- Subtasks:
  1. `P04-T06-S01` Select the representative dataset slice for semantic promotion.
     Depends on: P04-T02-S04, P04-T04-S04, P04-T05-S04
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: semantic MVP cohort
  2. `P04-T06-S02` Materialize entities, relations, events, and redactions into planned stores and contracts.
     Depends on: P04-T06-S01
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: structured semantics dataset
  3. `P04-T06-S03` Validate end-to-end evidence links, review states, and downstream read paths.
     Depends on: P04-T06-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: semantic acceptance report
  4. `P04-T06-S04` Publish downstream-readiness notes for retrieval, graph, analytics, and UI teams.
     Depends on: P04-T06-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: downstream guidance
