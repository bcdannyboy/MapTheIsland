# Phase 07 - Controlled QA, Advanced Analytics UI, And Production Hardening

Status: planned

## Objective

Add controlled QA, advanced analytical surfaces, and the operational hardening required for pilot and production milestones.

## Architecture Traceability

- `Architecture_Plan.md` lines 411-462
- `Architecture_Plan.md` lines 245-253
- `Architecture_Plan.md` lines 385-409

## Entry Criteria

- evidence workbench MVP exists
- retrieval and graph infrastructure exist
- quality gates and evaluation baselines exist

## Exit Criteria

- controlled QA works with citations and abstention
- advanced analytics surfaces work under policy boundaries
- hardening, SLOs, runbooks, and release readiness are complete

## Phase Handoff Summary

- Consumes:
  - A-022 through A-029
  - evidence workbench MVP release candidate
  - evaluation and gate evidence from earlier phases
- Produces:
  - A-030 and A-031
  - advanced analyst surfaces
  - release-readiness package
- Blocking open questions:
  - OQ-03 restricted-role governance
  - OQ-04 release audience and pilot cohort
  - OQ-05 gold-set curation ownership
- Primary workstreams:
  - WS-08 QA, Advanced UX, And Release Engineering
  - WS-07 BFF And Web Application for UI integration
- Primary signoff roles:
  - release lead
  - application lead
  - policy/security lead
- Earliest safe parallel starts:
  - none beyond the current architecture scope; this phase closes the planned delivery program

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P07-T01 | planned | P05-T01, P05-T02, P06-T01, P03-T03 |
| P07-T02 | planned | P07-T01, P06-T04 |
| P07-T03 | planned | P05-T02, P05-T03, P05-T04, P06-T02 |
| P07-T04 | planned | P06-T07, P07-T02, P05-T06 |

## P07-T01 Build Controlled QA Orchestration And Evidence-Pack Assembly

- Status: planned
- Relevant constraints: AC-03, AC-08, AC-09, AC-10, AC-18
- Objective: assemble a controlled server-side QA path grounded in evidence packs and policy masking.
- Dependencies: blocking on P05-T01, P05-T02, P06-T01, and P03-T03
- Parallelization: parallelizable with early P07-T03 UI work
- Required external decisions: OQ-04
- Deliverables:
  - QA orchestration service path
  - evidence-pack assembly pipeline
  - policy-aware prompt assembly
- Acceptance criteria:
  - QA flow is server-side only
  - evidence packs are inspectable and reproducible
  - restricted context is excluded or masked according to policy
- Subtasks:
  1. `P07-T01-S01` Implement query classification and retrieval-orchestration flow.
     Depends on: P05-T01-S04, P05-T02-S03, P06-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T03-S01
     Concrete output: QA orchestration baseline
  2. `P07-T01-S02` Implement evidence-pack assembly with ranked source grouping and graph expansion controls.
     Depends on: P07-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T01-S03
     Concrete output: evidence-pack builder
  3. `P07-T01-S03` Implement policy-based masking and model-gateway request assembly.
     Depends on: P07-T01-S02, P03-T03-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T01-S02
     Concrete output: QA prompt assembly layer
  4. `P07-T01-S04` Validate reproducibility and policy safety of evidence-pack generation.
     Depends on: P07-T01-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: QA evidence-pack validation report

## P07-T02 Build Support Verification, Abstention, And Citation UX

- Status: planned
- Relevant constraints: AC-03, AC-08, AC-10, AC-18
- Objective: ensure QA output can justify itself and abstain when it cannot.
- Dependencies: blocking on P07-T01 and P06-T04
- Parallelization: parallelizable with P07-T03
- Required external decisions: none
- Deliverables:
  - support-verification layer
  - abstention logic
  - citation mapping and navigation UX
- Acceptance criteria:
  - every answer has a support state
  - insufficient support results in abstention
  - citations jump to highlighted evidence
- Subtasks:
  1. `P07-T02-S01` Define support states and evidence-sufficiency rules.
     Depends on: P07-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T03-S02
     Concrete output: support-state model
  2. `P07-T02-S02` Implement support verification and abstention handling in the backend.
     Depends on: P07-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T02-S03
     Concrete output: abstention backend
  3. `P07-T02-S03` Implement citation map rendering and deep-link navigation into the document viewer.
     Depends on: P07-T02-S01, P06-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T02-S02
     Concrete output: citation UX
  4. `P07-T02-S04` Validate abstention behavior, citation accuracy, and restricted-content safety.
     Depends on: P07-T02-S02, P07-T02-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: QA support validation report

## P07-T03 Build Advanced Analytics UI, Graph Explorer, Topic Atlas, And Restricted Redaction Atlas

- Status: planned
- Relevant constraints: AC-03, AC-10, AC-11, AC-12, AC-18
- Objective: expose advanced evidence-backed analytical views without compromising policy or evidentiary clarity.
- Dependencies: blocking on P05-T02, P05-T03, P05-T04, and P06-T02
- Parallelization: parallelizable with P07-T01 and P07-T02
- Required external decisions: OQ-03, OQ-04
- Deliverables:
  - graph explorer
  - topic atlas
  - analytics dashboards
  - restricted redaction atlas
- Acceptance criteria:
  - graph edges distinguish evidence classes
  - topic and timeline views expose uncertainty and provenance
  - restricted features remain role-gated and policy-safe
- Subtasks:
  1. `P07-T03-S01` Implement graph explorer route and bounded subgraph rendering.
     Depends on: P05-T02-S04, P06-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T01-S01
     Concrete output: graph explorer
  2. `P07-T03-S02` Implement topic atlas and topic-over-time views.
     Depends on: P05-T04-S04, P06-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T02-S01
     Concrete output: topic atlas
  3. `P07-T03-S03` Implement timeline and saved analytics views over event-based backend outputs.
     Depends on: P05-T03-S04, P06-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T03-S02
     Concrete output: analytics views
  4. `P07-T03-S04` Implement restricted redaction atlas with explicit policy boundaries and validate safe handling.
     Depends on: P04-T05-S04, P03-T03-S04, P06-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T03-S03
     Concrete output: restricted redaction atlas

## P07-T04 Execute Hardening, Regression, SLO, And Release-Readiness Program

- Status: planned
- Relevant constraints: AC-07, AC-08, AC-17, AC-18
- Objective: complete the engineering, validation, operational, and release controls needed for preview, pilot, and production milestones.
- Dependencies: blocking on P06-T07, P07-T02, and P05-T06
- Parallelization: parallelizable with finishing work on P07-T03
- Required external decisions: OQ-03, OQ-04, OQ-05
- Deliverables:
  - regression suite
  - SLO dashboards and runbooks
  - backup, recovery, and rollback procedures
  - release-readiness report
- Acceptance criteria:
  - milestone gates are objectively testable
  - operations team has actionable runbooks
  - pilot or production release can be approved with documented evidence
- Subtasks:
  1. `P07-T04-S01` Execute the full regression and evaluation suite across evidence, retrieval, UI, and QA workflows.
     Depends on: P06-T07-S04, P07-T02-S04, P05-T06-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T03-S03
     Concrete output: release regression report
  2. `P07-T04-S02` Finalize SLO dashboards, alerts, and operational runbooks.
     Depends on: P07-T04-S01, P01-T06-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T04-S03
     Concrete output: operational readiness package
  3. `P07-T04-S03` Validate backup, recovery, rematerialization, and rollback procedures.
     Depends on: P07-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P07-T04-S02
     Concrete output: recovery validation report
  4. `P07-T04-S04` Produce pilot or production release-readiness decision package.
     Depends on: P07-T04-S02, P07-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: release-readiness package
