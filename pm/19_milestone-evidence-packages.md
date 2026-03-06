# Milestone Evidence Packages

This document makes go or no-go decisions concrete. A milestone is not reviewable until its evidence package is assembled.

## Package Template

Each milestone package must include:

- milestone scope statement
- exact included tasks and excluded tasks
- completed quality gates
- local and integration test reports with 100 percent pass rates
- coverage report demonstrating 100 percent handwritten-code coverage for included scope
- evaluation reports
- demo or walkthrough flows
- unresolved-risk list
- rollback and recovery evidence
- required signoffs

## R0 Planning Baseline Package

- required artifacts:
  - PM workspace
  - implementation baseline under `docs/implementation/`
  - dependency map
  - phase plan
  - risk register
  - decision log
  - research register
  - Phase 00 schema, policy, contract, and engineering baseline artifacts
  - local verification evidence for all handwritten code introduced during the baseline
- unresolved-risk tolerance:
  - planning-level open questions are allowed if explicitly recorded
- signoffs:
  - PM lead
  - architecture lead

## R1 Evidence Substrate Alpha Package

- required artifacts:
  - infrastructure bootstrap evidence
  - evidence ingest validation report
  - replay validation report
  - lineage validation evidence
  - ingest observability dashboard snapshot
- unresolved-risk tolerance:
  - no unresolved critical provenance risks
- signoffs:
  - platform or infrastructure lead
  - data and orchestration lead
  - document processing lead

## R2 Policy-Safe Evidence Workbench MVP Package

- required artifacts:
  - policy enforcement validation
  - review workflow validation
  - retrieval validation
  - search validation
  - document viewer validation
  - dossier validation
  - review workbench validation
- unresolved-risk tolerance:
  - no unresolved critical policy leakage or evidence-traceability risks
- signoffs:
  - policy and security lead
  - BFF and API lead
  - frontend lead
  - PM lead

## R3 Restricted Analyst Pilot Package

- required artifacts:
  - analytics and graph validation reports
  - pilot role configuration evidence
  - monitoring and alerting evidence
  - rollback and support runbooks
- unresolved-risk tolerance:
  - only explicitly accepted medium or lower residual risks
- signoffs:
  - policy and security lead
  - retrieval, graph, and analytics lead
  - evaluation and release lead

## R4 Controlled QA Preview Package

- required artifacts:
  - QA evidence-pack validation
  - support-verification and abstention validation
  - citation accuracy validation
  - QA regression report
- unresolved-risk tolerance:
  - no unresolved high risk related to hallucination, support failure, or policy leakage
- signoffs:
  - policy and security lead
  - BFF and API lead
  - evaluation and release lead

## R5 Production Readiness Package

- required artifacts:
  - full regression suite
  - SLO and alerting evidence
  - backup and recovery validation
  - rollback validation
  - release-readiness summary
- unresolved-risk tolerance:
  - only explicitly accepted low residual risks
- signoffs:
  - PM lead
  - architecture lead
  - platform or infrastructure lead
  - policy and security lead
  - evaluation and release lead
