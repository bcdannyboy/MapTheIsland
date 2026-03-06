# Phase 03 - Policy Enforcement, Review Loops, And Adjudication

Status: planned

## Objective

Establish the policy, access-control, review, and audit framework required before higher-level semantics and user-facing workflows can be safely promoted.

## Architecture Traceability

- `Architecture_Plan.md` lines 165-171
- `Architecture_Plan.md` lines 205-213
- `Architecture_Plan.md` lines 245-259
- `Architecture_Plan.md` lines 411-454

## Entry Criteria

- canonical evidence layer exists
- identity foundation exists
- policy taxonomy baseline exists

## Exit Criteria

- sensitivity pass operational
- role and policy enforcement operational
- review queues and adjudication events operational
- export and audit controls operational

## Phase Handoff Summary

- Consumes:
  - A-007 through A-010
  - Phase 01 identity baseline
  - policy taxonomy from Phase 00
- Produces:
  - A-011 through A-015
  - enforced role and export boundaries for later phases
- Blocking open questions:
  - OQ-03 restricted-role governance
  - OQ-04 release audience and pilot cohort where route visibility decisions depend on audience
- Primary workstreams:
  - WS-04 Policy, Security, And Review
- Primary signoff roles:
  - policy/security lead
  - architecture lead for policy model integrity
  - application lead for rendered access boundaries
- Earliest safe parallel starts:
  - Phase 04 extraction may continue during late policy integration, but production promotion remains blocked until this phase is signed off

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P03-T01 | planned | P02-T04, P00-T03 |
| P03-T02 | planned | P01-T07, P00-T03 |
| P03-T03 | planned | P03-T02, P01-T04 |
| P03-T04 | planned | P03-T01, P03-T02, P00-T02 |
| P03-T05 | planned | P03-T04 |

## P03-T01 Build Sensitivity Tagging And Restricted-Span Handling

- Status: planned
- Relevant constraints: AC-02, AC-07, AC-08, AC-10, AC-12
- Objective: classify spans by safe-handling category before broad indexing or semantic promotion.
- Dependencies: blocking on P02-T04 and P00-T03
- Parallelization: parallelizable with P03-T02
- Required external decisions: OQ-03 for restricted-role governance
- Deliverables:
  - sensitivity pipeline
  - restricted-span handling rules
  - masking and redaction-neighbor handling baseline
- Acceptance criteria:
  - required sensitivity enums are populated
  - restricted contexts are marked before higher-level pipelines consume them
  - broad-access indices can exclude or mask restricted content
- Subtasks:
  1. `P03-T01-S01` Implement deterministic recognizers and rule baselines for sensitive content.
     Depends on: P02-T07-S04, P00-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T02-S01
     Concrete output: deterministic sensitivity lane
  2. `P03-T01-S02` Integrate Presidio and custom recognizers into the sensitivity pass.
     Depends on: P03-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T01-S03
     Concrete output: enhanced sensitivity pipeline
  3. `P03-T01-S03` Define masking, hashing, and exclusion behavior for restricted spans and redaction neighborhoods.
     Depends on: P03-T01-S01, P00-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T01-S02
     Concrete output: restricted-handling rules
  4. `P03-T01-S04` Validate that restricted spans are correctly classified and isolated on a sample corpus.
     Depends on: P03-T01-S02, P03-T01-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: sensitivity validation report

## P03-T02 Implement Policy Engine And Role Model Across Services

- Status: planned
- Relevant constraints: AC-07, AC-08, AC-09, AC-10, AC-15
- Objective: establish consistent role and policy decisions across the BFF and backend services.
- Dependencies: blocking on P01-T07 and P00-T03
- Parallelization: parallelizable with P03-T01 and P03-T04
- Required external decisions: OQ-03, OQ-04
- Deliverables:
  - policy-decision model
  - role mapping implementation
  - service-level policy integration plan
- Acceptance criteria:
  - roles and policy outcomes are explicit
  - services can request policy decisions consistently
  - policy context can be surfaced to UI consumers
- Subtasks:
  1. `P03-T02-S01` Formalize role capabilities and policy decision inputs.
     Depends on: P01-T07-S02, P00-T03-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T01-S01
     Concrete output: role/policy model
  2. `P03-T02-S02` Implement OPA or equivalent policy execution baseline for service-side checks.
     Depends on: P03-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T04-S01
     Concrete output: policy engine baseline
  3. `P03-T02-S03` Define policy context payloads for BFF responses and downstream services.
     Depends on: P03-T02-S01, P00-T04-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T01-S03 later
     Concrete output: policy context contract
  4. `P03-T02-S04` Validate representative allow, deny, and restrict decisions.
     Depends on: P03-T02-S02, P03-T02-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: policy decision test suite

## P03-T03 Enforce Datastore-Level Access Controls And Export Rules

- Status: planned
- Relevant constraints: AC-09, AC-10, AC-12, AC-15
- Objective: enforce least-privilege reads and trusted-write patterns across all major stores and exports.
- Dependencies: blocking on P03-T02 and P01-T04
- Parallelization: parallelizable with P03-T04
- Required external decisions: OQ-03
- Deliverables:
  - PostgreSQL RLS strategy
  - OpenSearch read/write restriction strategy
  - Neo4j and Trino access controls
  - export-control rules
- Acceptance criteria:
  - datastore filtering aligns with application policy
  - write paths remain service-only where required
  - export policy is stricter than view policy
- Subtasks:
  1. `P03-T03-S01` Implement PostgreSQL row-level security and service-account boundaries.
     Depends on: P03-T02-S02, P01-T04-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T03-S02
     Concrete output: PostgreSQL enforcement
  2. `P03-T03-S02` Implement OpenSearch read filtering and trusted-write path rules.
     Depends on: P03-T02-S02, P01-T04-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T03-S01
     Concrete output: OpenSearch enforcement
  3. `P03-T03-S03` Implement Neo4j and Trino access-control baselines.
     Depends on: P03-T02-S02, P01-T04-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T03-S01, P03-T03-S02
     Concrete output: graph/query enforcement
  4. `P03-T03-S04` Define export-control workflow and validate least-privilege behavior end to end.
     Depends on: P03-T03-S01, P03-T03-S02, P03-T03-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: export enforcement validation

## P03-T04 Build Review API, Queues, Adjudication State, And Events

- Status: planned
- Relevant constraints: AC-07, AC-16, AC-17, AC-18
- Objective: create the human-review substrate that governs low-confidence and high-impact outputs.
- Dependencies: blocking on P03-T01, P03-T02, and P00-T02
- Parallelization: parallelizable with P03-T03
- Required external decisions: OQ-03, OQ-05
- Deliverables:
  - review queue model
  - adjudication API
  - adjudication events
  - downstream invalidation path
- Acceptance criteria:
  - review items can be created, claimed, resolved, and audited
  - adjudications are persistent and versioned
  - downstream asset invalidation/rematerialization hooks exist
- Subtasks:
  1. `P03-T04-S01` Define queue types, queue-item schema, and review-state transitions.
     Depends on: P03-T01-S04, P03-T02-S01, P00-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P02-T03-S04
     Concrete output: review-state model
  2. `P03-T04-S02` Implement review and adjudication API endpoints with audit-friendly persistence.
     Depends on: P03-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T04-S03
     Concrete output: review API
  3. `P03-T04-S03` Emit review and adjudication events for downstream re-materialization.
     Depends on: P03-T04-S02, P01-T05-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T04-S02
     Concrete output: adjudication events
  4. `P03-T04-S04` Validate one end-to-end review workflow including downstream invalidation.
     Depends on: P03-T04-S02, P03-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: review workflow validation

## P03-T05 Implement Audit Logging, Traceability, And Review Metrics

- Status: planned
- Relevant constraints: AC-04, AC-07, AC-17, AC-18
- Objective: make policy-sensitive activity observable, traceable, and measurable.
- Dependencies: blocking on P03-T04
- Parallelization: parallelizable with final portions of P03-T03
- Required external decisions: none
- Deliverables:
  - audit log schema
  - review metrics
  - traceability dashboards
- Acceptance criteria:
  - sensitive actions are auditable
  - review throughput and backlog are measurable
  - policy-denied requests are visible
- Subtasks:
  1. `P03-T05-S01` Define audit event schema for review, export, policy deny, and sensitive-access actions.
     Depends on: P03-T04-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T03-S04
     Concrete output: audit schema
  2. `P03-T05-S02` Implement storage and retrieval path for audit events.
     Depends on: P03-T05-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T05-S03
     Concrete output: audit persistence
  3. `P03-T05-S03` Define and publish review metrics and queue-health dashboards.
     Depends on: P03-T04-S04, P01-T06-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P03-T05-S02
     Concrete output: review metrics dashboards
  4. `P03-T05-S04` Validate traceability from adjudication to downstream asset change.
     Depends on: P03-T05-S02, P03-T05-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: adjudication traceability report
