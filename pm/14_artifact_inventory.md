# Artifact Inventory

This file centralizes artifact definitions, truth-layer placement, system-of-record choices, producer tasks, consumer tasks, and promotion rules. It exists so future contributors do not have to reconstruct artifact semantics from scattered backlog entries.

## Artifact Rules

- Every artifact must have one truth layer.
- Every artifact must have one system of record.
- Every artifact must have a clearly named producer.
- Every artifact must name the downstream consumers that rely on it.
- If promotion or review is required, that rule must be explicit.

## Evidence And Control Artifacts

| Artifact ID | Artifact | Truth Layer | System Of Record | Primary Producers | Primary Consumers | Promotion Rule |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | raw evidence object | raw evidence | object storage + lakeFS | P02-T01 | P02-T02, audit/replay paths | immutable on write; never edited in place |
| A-002 | ingest manifest record | raw evidence control | PostgreSQL + Iceberg | P02-T02 | P02-T05, operators, analytics | accepted when provenance and hash fields validate |
| A-003 | duplicate set | extracted control | PostgreSQL + Iceberg | P02-T02 | P02-T05, docproc, analytics | retained even if canonical representative changes |
| A-004 | page image | raw evidence derivative | object storage + canonical page asset | P02-T03, P02-T04 | document viewer, review workbench | always retained when page exists |
| A-005 | native text page output | extracted evidence | Iceberg + page asset linkage | P02-T03, P02-T04 | document viewer, extraction pipelines | promoted only with extractor identity and confidence |
| A-006 | OCR text page output | extracted evidence | Iceberg + page asset linkage | P02-T03, P02-T04 | document viewer, extraction pipelines, review | promoted only with OCR metadata and confidence |
| A-007 | canonical `Document` record | extracted evidence | Iceberg + PostgreSQL mirror | P02-T04 | all downstream phases | blocked if provenance contract incomplete |
| A-008 | canonical `Page` record | extracted evidence | Iceberg + PostgreSQL mirror | P02-T04 | all downstream phases | blocked if image/native/OCR linkage incomplete |
| A-009 | canonical `Span` record | extracted evidence | Iceberg + PostgreSQL mirror | P02-T04 | sensitivity, extraction, retrieval, QA | blocked if extractor identity missing |
| A-010 | validation checkpoint result | control | Great Expectations output + internal docs | P02-T05, P05-T06, P07-T04 | release gating, operators | required for gate progression |

## Policy And Review Artifacts

| Artifact ID | Artifact | Truth Layer | System Of Record | Primary Producers | Primary Consumers | Promotion Rule |
| --- | --- | --- | --- | --- | --- | --- |
| A-011 | sensitivity annotation | extracted control | PostgreSQL + Iceberg fields | P03-T01 | indexing, BFF, review, QA | required before unrestricted promotion |
| A-012 | policy decision result | interaction/control | policy engine logs + service response payloads | P03-T02, P03-T03, P06-T01, P07-T01 | BFF, export, QA, audit | advisory only until enforced in service path |
| A-013 | review item | interaction/control | PostgreSQL | P03-T04 | review workbench, metrics, downstream rematerialization | must carry queue type and review state |
| A-014 | adjudication record | control | PostgreSQL | P03-T04 | downstream rematerialization, audit, evaluation | accepted adjudications may promote downstream assets |
| A-015 | audit event | control | PostgreSQL or audit log sink | P03-T05 and sensitive services | operators, policy reviews, release signoff | append-only once written |

## Semantic Artifacts

| Artifact ID | Artifact | Truth Layer | System Of Record | Primary Producers | Primary Consumers | Promotion Rule |
| --- | --- | --- | --- | --- | --- | --- |
| A-016 | entity candidate | extracted claim | PostgreSQL + Iceberg | P04-T01 | P04-T02, review, dossiers | not canonical until resolution path completes |
| A-017 | alias candidate | extracted claim | PostgreSQL + Iceberg | P04-T01 | P04-T02, review | not canonical until reviewed or accepted |
| A-018 | canonical entity | extracted claim | PostgreSQL + graph projection inputs | P04-T02 | graph, retrieval, UI, QA | high-impact merges require adjudication |
| A-019 | relation record | extracted claim | Iceberg + PostgreSQL | P04-T03 | event extraction, graph, UI, QA | invalid if source span or schema type is missing |
| A-020 | event record | extracted claim | Iceberg + PostgreSQL + graph inputs | P04-T04 | graph, analytics, dossiers, QA | must preserve interval uncertainty and evidence links |
| A-021 | redaction object | extracted claim with policy risk | PostgreSQL + Iceberg | P04-T05 | redaction analytics, review, restricted UI | masked-context rules are mandatory |

## Analytical Artifacts

| Artifact ID | Artifact | Truth Layer | System Of Record | Primary Producers | Primary Consumers | Promotion Rule |
| --- | --- | --- | --- | --- | --- | --- |
| A-022 | retrieval artifact | hypothesis/derived | OpenSearch + supporting metadata store | P05-T01 | search, QA, BFF | never treated as evidence |
| A-023 | graph projection | hypothesis/derived | Neo4j | P05-T02 | graph explorer, QA, dossiers | rematerialized when upstream semantics change |
| A-024 | analytics table | hypothesis/derived | Iceberg + Trino | P05-T03 | analytics endpoints, dashboards, timeline views | must derive from event-centric inputs |
| A-025 | topic artifact | hypothesis/derived | Iceberg/OpenSearch/metadata store as defined later | P05-T04 | topic atlas, analytics, QA | may not be promoted as fact |
| A-026 | weak label output | hypothesis/derived | PostgreSQL + Iceberg + MLflow tracking | P05-T05 | analytics, review, QA-adjacent workflows | precision-calibrated before promotion |
| A-027 | experiment or evaluation result | control | MLflow | P05-T06, P07-T04 | release gates, model selection, audits | required for model-assisted release claims |

## Interaction Artifacts

| Artifact ID | Artifact | Truth Layer | System Of Record | Primary Producers | Primary Consumers | Promotion Rule |
| --- | --- | --- | --- | --- | --- | --- |
| A-028 | BFF response envelope | interaction | BFF runtime | P06-T01 | web application | must include policy/provenance fields where relevant |
| A-029 | saved search or saved analytics view | interaction | PostgreSQL or app metadata store to be finalized | P06-T02, P06-T03, P07-T03 | analysts, dashboards | promotion rules depend on export/view policy |
| A-030 | QA evidence pack | interaction/derived | PostgreSQL or cached metadata store to be finalized in implementation spec | P07-T01 | QA workspace, review, audit | reproducibility and policy masking are mandatory |
| A-031 | QA answer artifact | interaction/derived | QA service output + audit/log storage | P07-T02 | QA workspace, audit | invalid if no support state or citation map exists |

## Contract And Policy Baseline Artifacts

| Artifact ID | Artifact | Truth Layer | System Of Record | Primary Producers | Primary Consumers | Promotion Rule |
| --- | --- | --- | --- | --- | --- | --- |
| A-032 | synchronous API contract package | control | `libs/contracts` + implementation docs | P00-T04, P01-T01, P06-T01 | BFF, web app, internal service consumers | breaking changes require compatibility review and major-version increment |
| A-033 | async event contract package | control | `libs/contracts` + implementation docs | P00-T04, P01-T01, P01-T05, P03-T04 | event producers, event consumers, orchestration | event meaning may not change silently; breaking changes require new major version or event type |
| A-034 | policy taxonomy and capability matrix | control | `libs/policy` + implementation docs | P00-T03, P01-T01 | BFF, review API, retrieval, QA, web app | deny-by-default until restricted-role governance is approved |
| A-035 | GitOps control-plane application manifest set | control | repo Git + Argo CD `Application` and `AppProject` objects | P01-T03 | platform operators, Local control-plane reconciliation, later environment promotion work | Local only until higher-environment target exists and live tracked-remote reconciliation is validated |
| A-036 | Local secret bootstrap material | control | gitignored `.state/kind/` files + operator-namespace bootstrap secret | P01-T03 | Local Vault bootstrap, External Secrets Local validation only | never promoted; regenerated or rotated per workstation and may not be committed to Git |
| A-037 | Local certificate issuer and service certificate set | control | repo manifests + cert-manager-managed Kubernetes secrets | P01-T03 | Local sample workloads, later Local state-plane validation | Local only; not authoritative for higher-environment trust or public exposure |

## Notes On Systems Of Record

- Where the implementation spec has not yet fixed a low-level storage detail, the intended storage class is still identified here and the remaining decision is tracked explicitly rather than assumed.
- If a later design change alters a system of record, update this file and the decision log together.

## References

- [`Architecture_Plan.md`](../Architecture_Plan.md): lines 60-109, 131-171, 173-243, 245-289, 321-446
- [`07_decision_log.md`](./07_decision_log.md)
- [`08_research_register.md`](./08_research_register.md)
