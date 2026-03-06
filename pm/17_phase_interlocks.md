# Phase Interlocks And Handoffs

This document exists to make phase-to-phase boundaries explicit. It tells future contributors what each phase consumes, what it must produce, who primarily signs it off, and what the next phase is allowed to start before full completion.

## Phase 00

- Consumes:
  - architecture document
  - official-source research
- Produces:
  - implementation spec baseline
  - schema baseline
  - policy baseline
  - service-boundary baseline
  - PM control artifacts
- Primary accountable roles:
  - program manager
  - architecture lead
  - policy/security lead
- Primary signoff condition:
  - later phases no longer need to infer contracts or rules
- Next phase may start early:
  - Phase 01 repo scaffolding can begin once service boundaries and repo standards are stable

## Phase 01

- Consumes:
  - Phase 00 contracts and standards
- Produces:
  - deployable platform substrate
  - stateful-service baseline
  - identity baseline
  - CI and observability baseline
- Primary accountable roles:
  - platform lead
  - data plane lead
- Primary signoff condition:
  - later phases can build against stable environments and service foundations
- Next phase may start early:
  - Phase 02 harvester and ingest work may begin once object storage, lakeFS, PostgreSQL, and Dagster are operational

## Phase 02

- Consumes:
  - Phase 01 platform substrate
  - Phase 00 schema/provenance contracts
- Produces:
  - raw evidence control plane
  - canonical `Document`, `Page`, and `Span` assets
  - evidence validation and replay controls
- Primary accountable roles:
  - data plane lead
  - document-processing lead
- Primary signoff condition:
  - downstream phases can read accepted evidence objects without reconstructing lineage logic themselves
- Next phase may start early:
  - Phase 03 policy work may begin against sample evidence assets
  - Phase 04 extraction prototyping may begin on accepted evidence cohorts only

## Phase 03

- Consumes:
  - accepted evidence assets
  - identity foundation
  - policy baseline
- Produces:
  - sensitivity annotations
  - policy enforcement path
  - review and adjudication substrate
  - audit trail
- Primary accountable roles:
  - policy/security lead
  - application lead for policy surfaces
- Primary signoff condition:
  - higher-level features cannot leak restricted content or bypass review
- Next phase may start early:
  - Phase 04 extraction can proceed on evidence assets while final policy enforcement finishes, but promotion remains blocked until Phase 03 signoff

## Phase 04

- Consumes:
  - accepted evidence assets
  - sensitivity and review infrastructure
- Produces:
  - entities
  - aliases
  - relations
  - events
  - redaction objects
- Primary accountable roles:
  - semantics lead
  - policy/security lead for redaction handling
- Primary signoff condition:
  - downstream analytical layers can rely on event-centric, review-aware semantics
- Next phase may start early:
  - retrieval, graph, and topic research can begin on pilot semantic outputs, but release promotion waits for semantic signoff

## Phase 05

- Consumes:
  - structured semantics
  - policy enforcement
- Produces:
  - retrieval indices
  - graph projections
  - analytics tables
  - topic artifacts
  - weak-label artifacts
  - experiment and evaluation baselines
- Primary accountable roles:
  - retrieval/analytics lead
  - semantics lead for evaluation and calibration
- Primary signoff condition:
  - analyst-facing search and analytical views are explainable and safe
- Next phase may start early:
  - BFF work can begin against stable endpoint contracts and early search/data services

## Phase 06

- Consumes:
  - retrieval and data services
  - policy context rules
  - evidence and semantics read paths
- Produces:
  - evidence workbench MVP
  - analyst routes and workflows
  - review and job-management UX
- Primary accountable roles:
  - application lead
  - policy/security lead for rendered access boundaries
- Primary signoff condition:
  - analysts can do meaningful evidence work without hidden system behavior
- Next phase may start early:
  - controlled QA prototyping can begin once BFF, retrieval, and document-viewer deep-linking are stable

## Phase 07

- Consumes:
  - evidence workbench MVP
  - retrieval/graph/analytics substrates
  - quality baselines and evaluation harnesses
- Produces:
  - controlled QA
  - advanced analytics views
  - pilot and production readiness evidence
- Primary accountable roles:
  - release lead
  - application lead
  - policy/security lead
- Primary signoff condition:
  - release decisions can be made on objective evidence rather than optimism
- No later phase:
  - this is the hardening and release-readiness phase of the current architecture scope

## References

- [`03_phase_plan.md`](./03_phase_plan.md)
- [`04_dependency_map.md`](./04_dependency_map.md)
- [`05_workstream_index.md`](./05_workstream_index.md)
- relevant phase backlog files under [`backlog/`](./backlog)
