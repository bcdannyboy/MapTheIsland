# Roles And Responsibilities

This file defines ownership by role, not by named person. It exists so work can be assigned without leaving accountability ambiguous.

## PM Lead

- owns:
  - sequencing
  - dashboard state
  - backlog hygiene
  - dependency escalation
- approves:
  - cross-phase re-sequencing
  - release scope changes

## Architecture Lead

- owns:
  - architecture fidelity
  - contract coherence
  - system-of-record boundaries
  - cross-workstream technical consistency
- approves:
  - schema changes
  - service-boundary changes
  - artifact-authority changes

## Platform Or Infrastructure Lead

- owns:
  - Terraform and cluster baseline
  - GitOps
  - secrets and certificates
  - stateful service operations
- approves:
  - infrastructure readiness
  - environment promotion readiness

## Data And Orchestration Lead

- owns:
  - object lifecycle
  - lakeFS
  - Iceberg and Trino
  - Dagster assets
  - event contracts
- approves:
  - asset lineage completeness
  - replay or rematerialization readiness

## Document Processing Lead

- owns:
  - harvester
  - downloader
  - manifest
  - routing
  - PDF and OCR lanes
  - canonical evidence production
- approves:
  - evidence-layer MVP quality

## Policy And Security Lead

- owns:
  - sensitivity logic
  - role model
  - policy engine
  - datastore enforcement
  - export restrictions
  - audit coverage
- approves:
  - restricted-content handling
  - policy-sensitive release safety

## Review Operations Lead

- owns:
  - review queue definitions
  - adjudication behavior
  - queue metrics
  - escalation paths for low-confidence or sensitive outputs
- approves:
  - review workflow readiness

## Semantics Or NLP Lead

- owns:
  - entity extraction
  - alias handling
  - identity resolution
  - relation extraction
  - event extraction
  - weak supervision
- approves:
  - semantic dataset promotion
  - model-threshold changes with evaluation support

## Retrieval, Graph, And Analytics Lead

- owns:
  - search and rerank
  - graph materialization
  - analytics tables
  - topic pipeline
  - evidence-pack dependencies
- approves:
  - retrieval readiness
  - graph semantics readiness

## BFF And API Lead

- owns:
  - FastAPI orchestration
  - endpoint contracts
  - response envelopes
  - backend integration boundaries
- approves:
  - UI-facing API readiness

## Frontend Lead

- owns:
  - application shell
  - search UI
  - document viewer
  - dossier pages
  - graph and analytics views
  - review workbench UX
- approves:
  - analyst workflow readiness

## Evaluation And Release Lead

- owns:
  - quality gates
  - evaluation suites
  - regression baselines
  - SLO dashboards
  - release-readiness packages
- approves:
  - pilot and production readiness

## Assignment Rule

Each subagent or contributor should be assigned to one primary owner role for a work package. If the work package crosses multiple roles, split it unless the dependency map explicitly requires a combined package.
