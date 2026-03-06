# Phase 00 - Constraints And Implementation Specification

Status: done

## Objective

Translate the architecture into executable contracts, schemas, policy rules, and delivery standards so no later phase proceeds on implicit assumptions.

## Architecture Traceability

- `Architecture_Plan.md` lines 7-18
- `Architecture_Plan.md` lines 131-171
- `Architecture_Plan.md` lines 205-223
- `Architecture_Plan.md` lines 255-289
- `Architecture_Plan.md` line 470

## Entry Criteria

- architecture document available
- PM workspace initialized

## Exit Criteria

- implementation spec baseline exists
- canonical schema baseline exists
- policy taxonomy baseline exists
- service boundary baseline exists
- repo and engineering standards baseline exists

## Phase Handoff Summary

- Consumes:
  - `Architecture_Plan.md`
  - official-source research recorded in `pm/08_research_register.md`
- Produces:
  - implementation-spec baseline
  - schema and provenance baseline
  - policy and review-state baseline
  - service-boundary and contract baseline
  - PM control artifacts
- Blocking open questions:
  - none for baseline drafting
  - OQ-03 affects final restricted-role governance details but should be tracked, not assumed
- Primary workstreams:
  - program management
  - architecture
  - policy/security
- Primary signoff roles:
  - program manager
  - architecture lead
  - policy/security lead
- Earliest safe parallel starts:
  - Phase 01 repo scaffold work after P00-T04 and P00-T05 stabilize

## Task Index

| Task ID | Status | Depends On |
| --- | --- | --- |
| P00-T01 | done | none |
| P00-T02 | done | P00-T01 |
| P00-T03 | done | P00-T01 |
| P00-T04 | done | P00-T01 |
| P00-T05 | done | P00-T01 |
| P00-T06 | done | none |

## P00-T01 Draft Implementation Spec And Architecture Traceability

- Status: done
- Relevant constraints: AC-01 through AC-18
- Objective: convert the narrative architecture into a structured implementation-spec baseline with section-by-section traceability.
- Dependencies: independent
- Parallelization: parallelizable with P00-T06; soft-parallelizable with P00-T05 after the section inventory exists
- Required external decisions: none
- Deliverables:
  - implementation-spec outline
  - architecture-to-workstream traceability map
  - gap list for unresolved implementation details
- Acceptance criteria:
  - every architecture section maps to at least one planned workstream or task
  - no mandatory architecture invariant is untracked
  - unresolved items are listed explicitly rather than assumed
- Implementation evidence in repo:
  - `docs/implementation/implementation-spec-baseline.md`
  - `docs/implementation/architecture-traceability-matrix.md`
  - `docs/implementation/open-implementation-gaps.md`
- Subtasks:
  1. `P00-T01-S01` Inventory every architecture section and convert it into a traceability row.
     Depends on: none
     Dependency classification: independent
     Parallelization: independent
     Concrete output: section inventory table
  2. `P00-T01-S02` Group architecture sections into delivery phases and workstreams.
     Depends on: P00-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T06-S02
     Concrete output: initial phase/workstream mapping
  3. `P00-T01-S03` Identify unresolved implementation details that must become decisions or open questions.
     Depends on: P00-T01-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T01-S02
     Concrete output: implementation gap list
  4. `P00-T01-S04` Publish the implementation-spec baseline and link it from the PM workspace.
     Depends on: P00-T01-S02, P00-T01-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T02-S01
     Concrete output: implementation spec baseline document

## P00-T02 Define Canonical Schemas, Provenance Tuple, And Review States

- Status: done
- Relevant constraints: AC-03, AC-04, AC-05, AC-07, AC-16
- Objective: define the core data contracts that govern evidence, claims, provenance, sensitivity, and review state.
- Dependencies: blocking on P00-T01
- Parallelization: parallelizable with P00-T03 after schema scope is clear
- Required external decisions: none
- Deliverables:
  - canonical data model baseline
  - provenance field contract
  - review-state enum baseline
  - shared schema publication plan
- Acceptance criteria:
  - `Document`, `Page`, `Span`, and `Claim` are defined with required fields
  - provenance tuple is explicit and mandatory
  - review states and sensitivity fields are versioned
- Implementation evidence in repo:
  - `libs/schemas/src/maptheisland_schemas/evidence.py`
  - `libs/schemas/src/maptheisland_schemas/__init__.py`
  - `tests/test_evidence_models.py`
  - `pyproject.toml`
- Subtasks:
  1. `P00-T02-S01` Translate architecture schema examples into formal contract candidates.
     Depends on: P00-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T03-S01
     Concrete output: schema draft
  2. `P00-T02-S02` Define the mandatory provenance tuple and field-level validation expectations.
     Depends on: P00-T02-S01
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: provenance contract
  3. `P00-T02-S03` Define review-state, confidence, and sensitivity enums across evidence and derived artifacts.
     Depends on: P00-T02-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T02-S02
     Concrete output: enum baseline
  4. `P00-T02-S04` Define how schemas are shared across services, UI, and validation tooling.
     Depends on: P00-T02-S02, P00-T02-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T04-S03
     Concrete output: schema publication strategy

## P00-T03 Define Policy Taxonomy And Safety Model

- Status: done
- Relevant constraints: AC-02, AC-07, AC-08, AC-10, AC-12, AC-15
- Objective: convert the architecture’s safety rules into explicit policy categories, review triggers, and prohibited flows.
- Dependencies: blocking on P00-T01
- Parallelization: parallelizable with P00-T02
- Required external decisions: OQ-03 restricted-role governance path
- Deliverables:
  - sensitivity taxonomy
  - role and export-control matrix baseline
  - prohibited-flow catalog
  - initial policy test matrix
- Acceptance criteria:
  - restricted and unsafe-for-LLM states are defined
  - role-based access intent is explicit
  - no prohibited behavior is left implicit
- Implementation evidence in repo:
  - `docs/implementation/policy-taxonomy-and-safety-model.md`
  - `libs/policy/README.md`
- Subtasks:
  1. `P00-T03-S01` Enumerate all sensitivity classes and restricted-context cases named by the architecture.
     Depends on: P00-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T02-S01
     Concrete output: sensitivity taxonomy draft
  2. `P00-T03-S02` Define role intent, export strictness, and review triggers.
     Depends on: P00-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T04-S01
     Concrete output: role/export matrix
  3. `P00-T03-S03` Define prohibited flows, especially around redactions, QA prompts, and model outputs.
     Depends on: P00-T03-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T03-S02
     Concrete output: prohibited-flow catalog
  4. `P00-T03-S04` Create the initial policy-verification matrix for implementation phases.
     Depends on: P00-T03-S02, P00-T03-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T05-S04
     Concrete output: policy test matrix

## P00-T04 Define Service Boundaries And Contract Strategy

- Status: done
- Relevant constraints: AC-05, AC-09, AC-15, AC-16, AC-18
- Objective: define service ownership, shared libraries, API surfaces, event contracts, and versioning rules.
- Dependencies: blocking on P00-T01
- Parallelization: parallelizable with P00-T03
- Required external decisions: none
- Deliverables:
  - service catalog
  - contract ownership model
  - API/event inventory
  - contract versioning rules
- Acceptance criteria:
  - each service named in the architecture has a scoped responsibility
  - browser-facing data access is BFF-mediated
  - event contracts are identified where cross-service async updates are required
- Implementation evidence in repo:
  - `docs/implementation/service-boundaries-and-contracts.md`
  - `docs/implementation/implementation-spec-baseline.md`
  - `libs/contracts/README.md`
  - `apps/web/README.md`
- Subtasks:
  1. `P00-T04-S01` Turn the architecture’s service list into a concrete service catalog with clear ownership boundaries.
     Depends on: P00-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T03-S02
     Concrete output: service catalog
  2. `P00-T04-S02` Define core synchronous API surfaces and asynchronous event surfaces.
     Depends on: P00-T04-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T02-S03
     Concrete output: API/event inventory
  3. `P00-T04-S03` Define shared libraries for contracts, schemas, prompts, policy, and evaluation.
     Depends on: P00-T04-S01, P00-T02-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T05-S01
     Concrete output: shared-lib strategy
  4. `P00-T04-S04` Define versioning and backward-compatibility rules for contracts.
     Depends on: P00-T04-S02, P00-T04-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: contract versioning policy

## P00-T05 Establish Repo Structure And Engineering Standards

- Status: done
- Relevant constraints: AC-16, AC-17, AC-18
- Objective: define how the codebase will be organized, tested, linted, typed, and reviewed.
- Dependencies: soft_dependency on P00-T01 and P00-T04
- Parallelization: task-level parallelization is aligned to `P00-T06`; only the unblocked bootstrap lane may overlap with `P00-T03`
- Required external decisions: none
- Deliverables:
  - monorepo directory standard
  - Python and frontend workspace standards
  - testing and CI conventions
  - contribution expectations
- Acceptance criteria:
  - repo layout matches the architecture
  - toolchain standards are explicit
  - testing, coverage, and documentation standards explicitly encode 100 percent handwritten-code coverage and 100 percent local and integration test pass-rate gates
  - validation obligations are known before coding starts
- Implementation evidence in repo:
  - `docs/implementation/engineering-standards-baseline.md`
  - root `pyproject.toml` with `uv` bootstrap, dev dependency group, Ruff, mypy, pytest, and 100 percent coverage enforcement
  - root `uv.lock`
  - root `package.json` and `pnpm-workspace.yaml`
  - `pnpm-lock.yaml`
  - `apps/web/README.md`
  - `apps/web/playwright.config.ts`
  - `apps/web/tests/unit/playwright-config.test.ts`
  - root `README.md`
- Subtasks:
  1. `P00-T05-S01` Finalize the monorepo folder structure for infra, services, apps, and libs.
     Depends on: P00-T04-S03
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T01-S01 once approved
     Concrete output: repo structure standard
  2. `P00-T05-S02` Define Python toolchain standards around `uv`, Ruff, mypy, and pytest.
     Depends on: P00-T01-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T05-S03
     Concrete output: Python engineering standard
  3. `P00-T05-S03` Define frontend workspace standards around `pnpm`, TypeScript, Playwright, and contract sharing.
     Depends on: P00-T04-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T05-S02
     Concrete output: frontend engineering standard
  4. `P00-T05-S04` Define baseline CI expectations and release-branch expectations.
     Depends on: P00-T05-S02, P00-T05-S03, P00-T03-S04
     Dependency classification: blocking
     Parallelization: parallelizable with P01-T06-S01
     Concrete output: CI/review standard with enforced coverage and pass-rate thresholds

## P00-T06 Build PM Workspace And Research Traceability

- Status: done
- Relevant constraints: AC-17, AC-18
- Objective: create a persistent planning layer for future sessions and contributors.
- Dependencies: independent
- Parallelization: independent
- Required external decisions: none
- Deliverables:
  - `/pm` workspace
  - research register
  - risk register
  - subagent operating rules
- Acceptance criteria:
  - PM workspace exists and is internally navigable
  - current architecture and research are traceable
  - future sessions can resume from the dashboard and backlog
- Subtasks:
  1. `P00-T06-S01` Create root PM documents.
     Depends on: none
     Dependency classification: independent
     Parallelization: independent
     Concrete output: root PM files
  2. `P00-T06-S02` Create dependency, risk, decision, and research traceability documents.
     Depends on: P00-T06-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T01-S02
     Concrete output: program control files
  3. `P00-T06-S03` Create subagent operating rules, templates, and checklists.
     Depends on: P00-T06-S01
     Dependency classification: blocking
     Parallelization: parallelizable with P00-T05-S02
     Concrete output: subagent docs
  4. `P00-T06-S04` Create initial session log and status baseline.
     Depends on: P00-T06-S02, P00-T06-S03
     Dependency classification: blocking
     Parallelization: independent
     Concrete output: initial continuity state
