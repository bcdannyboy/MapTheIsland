# Dependency Map

This file is the canonical cross-phase dependency map. Detailed subtask dependencies live in the phase backlog files, but this file controls task-to-task sequencing and the program critical path.

## Legend

- `blocking`: hard predecessor must complete first
- `soft_dependency`: predecessor improves readiness but does not block start
- `independent`: can start without a prior task in this program
- `parallelizable`: explicitly safe to run alongside the listed tasks
- `CP`: critical path item

## Critical Path Summary

Phase 01 cannot begin safely from Phase 00 until two prerequisite tracks complete:

- `P00-T01 -> P00-T02`
- `P00-T01 -> P00-T04`

From that point, the earliest release path continues as:

`P01-T02 -> P01-T04 -> P02-T01 -> P02-T04 -> P02-T07 -> P03-T01 -> P03-T04 -> P04-T01 -> P04-T04 -> P05-T01 -> P06-T01 -> P06-T03 -> P06-T04 -> P07-T01 -> P07-T02 -> P07-T04`

## Cross-Phase Task Dependency Table

| Task ID | Task | Dependency Type | Depends On | Parallelizable With | Critical Path |
| --- | --- | --- | --- | --- | --- |
| P00-T01 | Draft implementation spec and architecture traceability | independent | none | P00-T05, P00-T06 | yes |
| P00-T02 | Define canonical schemas, provenance tuple, and review states | blocking | P00-T01 | P00-T03 | yes |
| P00-T03 | Define policy taxonomy and safety model | blocking | P00-T01 | P00-T02, P00-T04 | no |
| P00-T04 | Define service boundaries and contract strategy | blocking | P00-T01 | P00-T03, P00-T05 | yes |
| P00-T05 | Establish repo structure and engineering standards | soft_dependency | P00-T01 | P00-T06 | no |
| P00-T06 | Build PM workspace and research traceability | independent | none | P00-T01, P00-T05 | no |
| P01-T01 | Scaffold monorepo and shared libraries | blocking | P00-T04, P00-T05 | P01-T02, P01-T06 | no |
| P01-T02 | Provision IaC and Kubernetes baseline | blocking | P00-T04 | P01-T01, P01-T03 | yes |
| P01-T03 | Configure GitOps, secrets, and certificate management | blocking | P01-T02 | P01-T06 | no |
| P01-T04 | Stand up core stateful services and catalogs | blocking | P01-T02, P01-T03, P00-T02 | P01-T05 | yes |
| P01-T05 | Establish orchestration, eventing, and model gateway baseline | blocking | P01-T04 | P01-T06 | no |
| P01-T06 | Establish CI/CD, linting, test, and observability skeleton | blocking | P01-T01 | P01-T03, P01-T05 | no |
| P01-T07 | Establish identity and access foundation | blocking | P01-T02, P00-T03 | P01-T06 | no |
| P02-T01 | Build harvester, downloader, and ingest-branch workflow | blocking | P01-T04, P01-T05 | P02-T02 | yes |
| P02-T02 | Build manifest, deduplication, and routing services | blocking | P02-T01, P00-T02 | P02-T03 | no |
| P02-T03 | Build PDF, layout, and OCR processing lanes | blocking | P02-T02 | P02-T04 | no |
| P02-T04 | Materialize canonical Document/Page/Span assets | blocking | P02-T03, P00-T02 | P02-T05 | yes |
| P02-T05 | Implement lineage, validation, and replay controls | blocking | P02-T04 | P02-T06 | no |
| P02-T06 | Build ingest observability and failure handling | blocking | P02-T01, P02-T03 | P02-T05 | no |
| P02-T07 | Produce evidence-layer MVP dataset and acceptance checks | blocking | P02-T04, P02-T05 | none | yes |
| P03-T01 | Build sensitivity tagging and restricted-span handling | blocking | P02-T04, P00-T03 | P03-T02 | yes |
| P03-T02 | Implement policy engine and role model across services | blocking | P01-T07, P00-T03 | P03-T03 | no |
| P03-T03 | Enforce datastore-level access controls and export rules | blocking | P03-T02, P01-T04 | P03-T04 | no |
| P03-T04 | Build review API, queues, adjudication state, and events | blocking | P03-T01, P03-T02, P00-T02 | P03-T05 | yes |
| P03-T05 | Implement audit logging, traceability, and review metrics | blocking | P03-T04 | P03-T03 | no |
| P04-T01 | Build entity and alias extraction pipeline | blocking | P02-T07, P03-T01 | P04-T02, P04-T03 | yes |
| P04-T02 | Build identity resolution and merge-review workflow | blocking | P04-T01, P03-T04 | P04-T03 | no |
| P04-T03 | Build thread reconstruction and relation extraction | blocking | P02-T07, P03-T01 | P04-T02, P04-T04 | no |
| P04-T04 | Build event extraction, temporal normalization, and event coreference | blocking | P04-T01, P04-T03 | P04-T05 | yes |
| P04-T05 | Build redaction object modeling and safe analytical handling | blocking | P02-T07, P03-T01 | P04-T04 | no |
| P04-T06 | Deliver structured semantics MVP dataset | blocking | P04-T02, P04-T04, P04-T05 | none | no |
| P05-T01 | Build retrieval indexing, embeddings, and rerank pipeline | blocking | P04-T06, P03-T03 | P05-T02, P05-T03 | yes |
| P05-T02 | Build graph schema materialization and graph-service queries | blocking | P04-T06, P03-T03 | P05-T01, P05-T03 | no |
| P05-T03 | Build event-based analytics tables and dashboards backend | blocking | P04-T04, P01-T04 | P05-T01, P05-T02 | no |
| P05-T04 | Build topic modeling and sense-induction research lane | soft_dependency | P04-T06 | P05-T01, P05-T03, P05-T05 | no |
| P05-T05 | Build weak supervision and calibration lane | soft_dependency | P04-T06, P03-T04 | P05-T04 | no |
| P05-T06 | Expand MLflow, evaluation, and data-quality checkpoints | blocking | P05-T01, P05-T03 | P05-T04, P05-T05 | no |
| P06-T01 | Build FastAPI BFF orchestration layer | blocking | P00-T04, P03-T03, P05-T01 | P06-T02 | yes |
| P06-T02 | Build Next.js shell, auth flow, and shared client state | blocking | P01-T07, P06-T01 | P06-T03, P06-T06 | no |
| P06-T03 | Build unified search experience | blocking | P06-T01, P05-T01 | P06-T02, P06-T04 | yes |
| P06-T04 | Build document viewer with image/native/OCR overlays | blocking | P06-T01, P02-T07 | P06-T03, P06-T05 | yes |
| P06-T05 | Build entity and event dossier surfaces | blocking | P06-T01, P04-T06 | P06-T04, P06-T06 | no |
| P06-T06 | Build review workbench and job-management flows | blocking | P06-T01, P03-T04 | P06-T02, P06-T05 | no |
| P06-T07 | Deliver evidence workbench MVP | blocking | P06-T03, P06-T04, P06-T05, P06-T06 | none | no |
| P07-T01 | Build controlled QA orchestration and evidence-pack assembly | blocking | P05-T01, P05-T02, P06-T01, P03-T03 | P07-T03 | yes |
| P07-T02 | Build support verification, abstention, and citation UX | blocking | P07-T01, P06-T04 | P07-T03 | yes |
| P07-T03 | Build advanced analytics UI, graph explorer, topic atlas, and restricted redaction atlas | blocking | P05-T02, P05-T03, P05-T04, P06-T02 | P07-T01, P07-T02 | no |
| P07-T04 | Execute hardening, regression, SLO, and release-readiness program | blocking | P06-T07, P07-T02, P05-T06 | P07-T03 | yes |

## Notes

- Topic modeling and weak supervision are intentionally not on the minimum credible release path.
- Review infrastructure is a hard prerequisite for safe promotion of high-impact semantic outputs.
- Evidence workbench MVP can ship before controlled QA.
- If a future decision changes the release boundary, update this file before changing any backlog.
