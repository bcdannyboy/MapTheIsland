# Phase 06 - Backend-For-Frontend And Evidence Workbench UI

Status: planned

## Objective

Expose the evidence layer and structured semantics through a policy-safe, inspectable analyst workbench.

## Architecture Traceability

- `Architecture_Plan.md` lines 293-377
- `Architecture_Plan.md` lines 379-448
- `Architecture_Plan.md` lines 450-462

## Entry Criteria

- minimum retrieval pipeline exists
- policy enforcement exists
- structured semantics exist

## Exit Criteria

- BFF exists
- Next.js shell exists
- search, document viewer, entity/event routes, and review workbench exist
- evidence workbench MVP is validated end to end

## Phase Handoff Summary

- Consumes:
  - A-007 through A-009
  - A-018 through A-024
  - A-028 once the BFF response envelope stabilizes
- Produces:
  - A-028 and A-029
  - evidence workbench MVP
  - analyst-facing routes and review workflows
- Blocking open questions:
  - OQ-04 release audience and pilot cohort
  - OQ-03 where role-restricted route behavior depends on governance
- Primary workstreams:
  - WS-07 BFF And Web Application
  - WS-04 Policy, Security, And Review for access-boundary enforcement
- Primary signoff roles:
  - application lead
  - policy/security lead
- Earliest safe parallel starts:
  - Phase 07 QA orchestration can begin once BFF orchestration, search, and viewer deep-linking are stable

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P06-T01 | planned | P00-T04, P03-T03, P05-T01 |
| P06-T02 | planned | P01-T07, P06-T01 |
| P06-T03 | planned | P06-T01, P05-T01 |
| P06-T04 | planned | P06-T01, P02-T07 |
| P06-T05 | planned | P06-T01, P04-T06 |
| P06-T06 | planned | P06-T01, P03-T04 |
| P06-T07 | planned | P06-T03, P06-T04, P06-T05, P06-T06 |

## P06-T01 Build FastAPI BFF Orchestration Layer

- Status: planned
- Relevant constraints: AC-05, AC-09, AC-10, AC-15, AC-18
- Objective: provide the single policy-aware orchestration surface between the browser and backend systems.
- Dependencies: blocking on P00-T04, P03-T03, and P05-T01
- Parallelization: parallelizable with P06-T02
- Required external decisions: OQ-04 if release audience shapes route scope
- Deliverables:
  - BFF service
  - service-client and query-orchestration layer
  - response envelope with policy and provenance context
- Acceptance criteria:
  - browser access is fully BFF-mediated
  - BFF can query required backends safely
  - core endpoints return policy and provenance metadata
- Subtasks:
  1. `P06-T01-S01` Implement the BFF service skeleton, dependency wiring, and service-client abstraction.
     Depends on: P00-T04-S02, P03-T03-S04, P05-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T02-S01
     Concrete output: BFF skeleton
  2. `P06-T01-S02` Implement endpoint contracts for documents, entities, events, search, graph, analytics, jobs, and review.
     Depends on: P06-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S01
     Concrete output: endpoint contract implementation
  3. `P06-T01-S03` Add response envelopes for `policy_context`, `provenance_summary`, and `result_confidence`.
     Depends on: P06-T01-S02, P03-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T02-S03
     Concrete output: response envelope layer
  4. `P06-T01-S04` Validate BFF auth, policy, and backend orchestration on representative routes.
     Depends on: P06-T01-S02, P06-T01-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: BFF validation record

## P06-T02 Build Next.js Shell, Auth Flow, And Shared Client State

- Status: planned
- Relevant constraints: AC-09, AC-15, AC-18
- Objective: build the web application shell, route structure, auth handling, and shared query-state patterns.
- Dependencies: blocking on P01-T07 and P06-T01
- Parallelization: parallelizable with P06-T03 and P06-T06
- Required external decisions: OQ-04
- Deliverables:
  - application shell
  - auth/session flow
  - shared client-state conventions
- Acceptance criteria:
  - route structure follows the architecture
  - auth state is mediated safely
  - query keys and route state are deterministic
- Subtasks:
  1. `P06-T02-S01` Create the Next.js route skeleton and shared layout shell.
     Depends on: P01-T07-S03, P06-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T01-S01
     Concrete output: app shell
  2. `P06-T02-S02` Implement auth/session integration and protected-route behavior.
     Depends on: P06-T02-S01, P01-T07-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T06-S01
     Concrete output: auth flow
  3. `P06-T02-S03` Implement TanStack Query patterns, query-key conventions, and job-polling helpers.
     Depends on: P06-T02-S01, P06-T01-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S02
     Concrete output: client-state framework
  4. `P06-T02-S04` Implement URL-state, filter-state, and saved-view baseline behavior.
     Depends on: P06-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S03
     Concrete output: route-state baseline

## P06-T03 Build Unified Search Experience

- Status: planned
- Relevant constraints: AC-03, AC-10, AC-18
- Objective: provide an inspectable unified search surface across major artifact classes.
- Dependencies: blocking on P06-T01 and P05-T01
- Parallelization: parallelizable with P06-T04
- Required external decisions: none
- Deliverables:
  - search page
  - tabbed result groups
  - explainable ranking controls
- Acceptance criteria:
  - search explains why results matched
  - result tabs cover the required artifact types
  - filters and ranking modes are explicit and reproducible
- Subtasks:
  1. `P06-T03-S01` Implement the search API integration and top-level query model.
     Depends on: P06-T01-S02, P05-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T02-S03
     Concrete output: search data integration
  2. `P06-T03-S02` Implement result tabs, card layouts, and grouped-result rendering.
     Depends on: P06-T03-S01, P06-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S03
     Concrete output: search UI layout
  3. `P06-T03-S03` Implement ranking-mode controls, filters, and explanation surfaces.
     Depends on: P06-T03-S01, P06-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S02
     Concrete output: search controls and explanations
  4. `P06-T03-S04` Validate search behavior for relevance, confidence, and policy filtering.
     Depends on: P06-T03-S02, P06-T03-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: search validation report

## P06-T04 Build Document Viewer With Image, Native, And OCR Overlays

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-10, AC-14, AC-18
- Objective: build the evidentiary center of the product around the document/page/span model.
- Dependencies: blocking on P06-T01 and P02-T07
- Parallelization: parallelizable with P06-T03 and P06-T05
- Required external decisions: none
- Deliverables:
  - PDF.js viewer integration
  - overlay model for text, entities, and claims/events
  - extraction-mode toggles
- Acceptance criteria:
  - analysts can switch among image, native text, and OCR layers
  - overlays are grounded in canonical page/span data
  - redaction visibility obeys policy rules
- Subtasks:
  1. `P06-T04-S01` Implement document and page retrieval integration in the BFF and UI.
     Depends on: P06-T01-S02, P02-T07-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T03-S01
     Concrete output: document page data flow
  2. `P06-T04-S02` Implement PDF.js rendering and canonical overlay placement.
     Depends on: P06-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T04-S03
     Concrete output: viewer and overlay engine
  3. `P06-T04-S03` Implement image/native/OCR toggles, jump-to-source behavior, and restricted redaction rendering.
     Depends on: P06-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T04-S02
     Concrete output: evidentiary honesty controls
  4. `P06-T04-S04` Validate source highlighting, extraction-mode honesty, and restricted rendering behavior.
     Depends on: P06-T04-S02, P06-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: document-viewer validation report

## P06-T05 Build Entity And Event Dossier Surfaces

- Status: planned
- Relevant constraints: AC-03, AC-04, AC-11, AC-18
- Objective: provide evidence-backed dossier and timeline views for entities and events.
- Dependencies: blocking on P06-T01 and P04-T06
- Parallelization: parallelizable with P06-T04 and P06-T06
- Required external decisions: none
- Deliverables:
  - entity route
  - event route
  - local timeline and evidence sections
- Acceptance criteria:
  - canonical facts and hypothesis-level associations are visually distinct
  - timelines use event participation rather than raw mentions alone
  - all surfaced objects can jump to supporting evidence
- Subtasks:
  1. `P06-T05-S01` Implement entity dossier data integration and page sections.
     Depends on: P06-T01-S02, P04-T06-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T05-S02
     Concrete output: entity dossier route
  2. `P06-T05-S02` Implement event page data integration and supporting evidence sections.
     Depends on: P06-T01-S02, P04-T06-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T05-S01
     Concrete output: event route
  3. `P06-T05-S03` Implement local timeline visualization and confidence or uncertainty display.
     Depends on: P06-T05-S01, P06-T05-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: dossier timeline components
  4. `P06-T05-S04` Validate evidence jumps, confidence presentation, and route reproducibility.
     Depends on: P06-T05-S03, P06-T04-S04
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: dossier validation report

## P06-T06 Build Review Workbench And Job-Management Flows

- Status: planned
- Relevant constraints: AC-07, AC-17, AC-18
- Objective: expose the review substrate to analysts and provide deterministic job-state UX for long-running operations.
- Dependencies: blocking on P06-T01 and P03-T04
- Parallelization: parallelizable with P06-T02 and P06-T05
- Required external decisions: OQ-04 if role scope affects queue access
- Deliverables:
  - review route
  - queue views
  - adjudication UX
  - job polling and status surfaces
- Acceptance criteria:
  - reviewers can work through queue items efficiently
  - adjudication actions are reflected in the UI
  - long-running job states are inspectable and deterministic
- Subtasks:
  1. `P06-T06-S01` Implement review queue data integration and route structure.
     Depends on: P06-T01-S02, P03-T04-S04, P06-T02-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T02-S03
     Concrete output: review route baseline
  2. `P06-T06-S02` Implement adjudication actions, confidence display, and prior-case suggestions if available.
     Depends on: P06-T06-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T06-S03
     Concrete output: adjudication UX
  3. `P06-T06-S03` Implement job polling, completion handling, and dependent-cache invalidation.
     Depends on: P06-T02-S03, P06-T01-S02
     Dependency classification: blocking
     Parallelization: parallelizable with P06-T06-S02
     Concrete output: job-management UX
  4. `P06-T06-S04` Validate one end-to-end review flow and one long-running job flow.
     Depends on: P06-T06-S02, P06-T06-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: review/job validation report

## P06-T07 Deliver Evidence Workbench MVP

- Status: planned
- Relevant constraints: AC-03, AC-08, AC-18
- Objective: produce the first credible analyst-facing release of the platform.
- Dependencies: blocking on P06-T03, P06-T04, P06-T05, and P06-T06
- Parallelization: none
- Required external decisions: OQ-04
- Deliverables:
  - evidence workbench MVP release candidate
  - acceptance report
  - onboarding and operator notes
- Acceptance criteria:
  - analysts can search, inspect documents, inspect entities/events, and adjudicate review queues
  - evidence links and policy context are visible
  - release candidate satisfies the evidence-workbench quality gate
- Subtasks:
  1. `P06-T07-S01` Run end-to-end analyst workflows across search, viewer, dossiers, and review.
     Depends on: P06-T03-S04, P06-T04-S04, P06-T05-S04, P06-T06-S04
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: end-to-end workflow report
  2. `P06-T07-S02` Validate role-based visibility and restricted-content behavior across the MVP.
     Depends on: P06-T07-S01
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: policy-safe MVP validation
  3. `P06-T07-S03` Publish operator notes, analyst onboarding notes, and known limitations.
     Depends on: P06-T07-S02
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: release notes
  4. `P06-T07-S04` Mark the MVP release candidate ready for hardening or preview.
     Depends on: P06-T07-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: MVP readiness decision
