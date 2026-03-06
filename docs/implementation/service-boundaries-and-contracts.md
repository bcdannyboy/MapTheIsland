# Service Boundaries And Contract Baseline

## Purpose

This document is the detailed `P00-T04` implementation baseline for service
ownership, browser-safe boundaries, synchronous API surfaces, asynchronous
integration events, and shared-library contract governance.

The architecture is explicit about two things that cannot remain informal:

- the browser is never trusted with privileged datastore or model access
- every cross-service contract must remain inspectable, versioned, and owned

This document therefore fixes the service boundary model that later Phase 01,
Phase 05, and Phase 06 work must inherit.

## Boundary Rules

- `bff` is the only browser-facing business API surface.
- Internal services are event-first by default and should not invent public
  business APIs without a documented reason.
- Service-local helper models may remain local, but anything that crosses a
  browser, process, queue, or storage boundary must be published through the
  shared contract layer.
- Health, readiness, metrics, version, and OpenAPI discovery endpoints are
  expected on every long-lived service once runtime implementation begins.
- Generated client types are derived artifacts; the authoritative contract
  sources remain `libs/schemas`, `libs/contracts`, `libs/policy`, and these
  implementation docs.

## Service Catalog

| Service | Primary Owner Role | First Delivery Phase | Primary Responsibility | Primary Writes | Explicit Non-Ownership |
| --- | --- | --- | --- | --- | --- |
| `harvester` | document processing lead | `P02` | discover official DOJ sources, re-check known sources, and create raw ingest work | source discovery records, ingest-discovery events | parsing, OCR, canonical evidence, search, UI |
| `docproc` | document processing lead | `P02` | classify files, parse PDFs, extract layout, and coordinate canonical evidence materialization | page assets, layout assets, canonical evidence jobs | role policy, semantic extraction, identity resolution |
| `ocr` | document processing lead | `P02` | execute OCR fallback lanes and emit OCR-confidence outcomes | OCR text assets, OCR-completion events | page canonicalization policy, semantic interpretation |
| `extractor` | semantics or NLP lead | `P04` | extract claims, entities, aliases, relations, redaction objects, and event candidates from accepted spans | semantic candidate assets, extraction events | canonical identity merges, graph projection, browser APIs |
| `resolver` | semantics or NLP lead | `P04` | perform identity resolution and prepare merge-review candidates | canonical entity mappings, merge proposals | raw extraction, browser orchestration, export policy |
| `topics` | retrieval, graph, and analytics lead | `P05` | materialize topic, sense, and weak-label research artifacts | topic artifacts, weak-label outputs | evidence truth, review adjudication, browser auth |
| `graph-builder` | retrieval, graph, and analytics lead | `P05` | build event-centric graph projections and bounded graph query assets | Neo4j projections, graph-refresh events | canonical truth ownership, browser rendering |
| `indexer` | retrieval, graph, and analytics lead | `P05` | materialize OpenSearch indices and retrieval artifacts from accepted evidence and semantics | retrieval artifacts, index-refresh events | evidence adjudication, UI response composition |
| `review-api` | review operations lead | `P03` | own review queues, adjudications, review-state changes, and review-driven invalidation events | adjudications, review audit records, invalidation events | browser auth, direct graph/search access, QA synthesis |
| `qa-orchestrator` | BFF and API lead with policy/security co-review | `P07` | assemble evidence packs, enforce support verification, apply abstention, and mediate model-gateway calls | QA evidence packs, QA answer artifacts, abstention records | browser session handling, canonical evidence storage |
| `bff` | BFF and API lead | `P06` | mediate analyst requests to trusted backends and return policy-aware, provenance-aware response envelopes | UI response envelopes, export requests, long-running job status | canonical evidence generation, direct datastore/browser trust bypass |

## Shared Infrastructure Dependencies

The following systems remain platform-level dependencies rather than service
ownership domains:

- object storage plus lakeFS for immutable evidence
- Iceberg for analytical assets
- PostgreSQL for operational state and adjudication
- OpenSearch for retrieval
- Neo4j for graph storage
- Trino for interactive analytical SQL
- Kafka for integration events
- Dagster for orchestration and rematerialization
- model gateway infrastructure for all model traffic

## Browser-Facing API Inventory

The architecture defines the browser-facing BFF surface explicitly. These
endpoints are the authoritative Phase 00 inventory for Phase 06 route planning:

| Endpoint | Method | Primary Consumer Route Or Flow | Primary Purpose | Required Envelope Notes |
| --- | --- | --- | --- | --- |
| `/search` | `GET` | `/search` | hybrid evidence retrieval across documents, entities, events, topics, threads, and redactions | include `policy_context`, `provenance_summary`, `result_confidence`, and explainability fields |
| `/documents/{document_id}` | `GET` | `/documents/[documentId]` | document-level evidence metadata and viewer bootstrap | include provenance summary and policy-rendering flags |
| `/documents/{document_id}/pages/{page_number}` | `GET` | `/documents/[documentId]` | page image, native text, OCR text, overlays, and jump targets | include overlay provenance and extraction-mode cues |
| `/entities/{entity_id}` | `GET` | `/entities/[entityId]` | entity dossier payload with canonical facts, candidates, and evidence timeline | include confidence and review-state summaries |
| `/events/{event_id}` | `GET` | `/events/[eventId]` | event detail payload with participants, interval uncertainty, and supporting spans | include interval-confidence details |
| `/topics/{topic_id}` | `GET` | `/topics/[topicId]` | topic atlas payload with exemplars and temporal drift views | include topic-version metadata and evidence counts |
| `/graph/subgraph` | `GET` | `/graph` | bounded server-generated subgraph retrieval | include graph filter summary and restricted-edge handling notes |
| `/analytics/timeseries` | `GET` | `/timeline` | time-series and interval analytics payloads | include aggregation window metadata and confidence notes |
| `/analytics/heatmap` | `GET` | analytics views | server-generated heatmap-style aggregations | include aggregation provenance and policy scope |
| `/qa/ask` | `POST` | `/qa` | controlled QA request handling | include support state, citation map, and abstention details |
| `/review/adjudications` | `POST` | `/review` | submit review decisions from the workbench | include actor, review context, and invalidation outcome |
| `/review/entity-merges` | `POST` | `/review` | submit merge-review decisions for entity resolution | include merge-review policy context |
| `/jobs/{job_id}` | `GET` | job polling across UI | deterministic job-status polling | include job class, progress, and blocking reason if any |
| `/exports/{export_id}` | `GET` | export and retrieval flows | export-status lookup and signed URL retrieval when allowed | include export policy outcome and short-lived URL state |

Every browser-facing business endpoint must return `policy_context`,
`provenance_summary`, and `result_confidence` when the route semantics make
them relevant. The browser must not infer or synthesize those fields.

## Internal Synchronous Surface Rules

The Phase 00 internal synchronous API rule is intentionally narrow:

- `review-api` may expose queue and adjudication endpoints for `bff`.
- `qa-orchestrator` may expose evidence-pack and answer-generation orchestration
  endpoints for `bff`.
- Other services should prefer asynchronous integration events plus direct
  datastore materialization rather than service-to-service business APIs.

When runtime implementation begins, every long-lived service must at minimum
expose:

- `GET /health/live`
- `GET /health/ready`
- `GET /metrics`
- `GET /version`
- `GET /openapi.json`

These are operational surfaces, not analyst-facing APIs.

## Async Event Inventory

The architecture names the event backbone conceptually. The following inventory
is the Phase 00 contract baseline for cross-service integration events:

| Event Type | Producer | Primary Consumers | Subject | Purpose |
| --- | --- | --- | --- | --- |
| `source.discovered` | `harvester` | orchestration, audit, ingest monitoring | source URL or discovery record | record lawful source discovery and re-discovery |
| `file.downloaded` | `harvester` | `docproc`, orchestration | raw evidence object | signal that immutable raw bytes now exist |
| `file.routed` | `docproc` | orchestration, audit | manifest or document candidate | record deterministic file classification and routing |
| `file.parsed` | `docproc` | `ocr`, orchestration | document or page set | signal native parse and layout extraction completion |
| `ocr.completed` | `ocr` | `docproc`, orchestration, review | page or OCR job | publish OCR outputs and fallback confidence state |
| `canonical.assets.materialized` | `docproc` | `extractor`, policy pipelines, indexing preparation | document, page, or span assets | announce accepted canonical evidence availability |
| `claims.extracted` | `extractor` | `resolver`, `graph-builder`, `indexer`, review | claim/entity/relation/event candidates | announce semantic candidate materialization |
| `entity.merge.proposed` | `resolver` | `review-api`, orchestration | merge candidate | open review for high-impact identity decisions |
| `adjudication.accepted` | `review-api` | `resolver`, `indexer`, `graph-builder`, evaluation | review item or promoted artifact | trigger downstream rematerialization from accepted review |
| `adjudication.rejected` | `review-api` | `resolver`, `indexer`, `graph-builder`, evaluation | review item or rejected artifact | trigger suppression, rollback, or alternate routing |
| `index.refreshed` | `indexer` | `bff`, QA, observability | retrieval artifact or index generation | announce retrieval refresh completion |
| `graph.projection.rebuilt` | `graph-builder` | `bff`, analytics, observability | graph projection generation | announce graph rematerialization completion |
| `topics.materialized` | `topics` | analytics, `bff`, evaluation | topic generation | announce topic artifact refresh |
| `qa.answer.recorded` | `qa-orchestrator` | audit, review, observability | QA request or answer artifact | record successful controlled QA completion |
| `qa.abstained` | `qa-orchestrator` | audit, review, observability | QA request or evidence pack | record policy or support-state abstention |

Every integration event must include this minimum envelope:

- `event_id`
- `event_type`
- `schema_version`
- `occurred_at`
- `producer`
- `subject_type`
- `subject_id`
- `trace_id`
- `causation_id` when emitted from a prior event or review action
- provenance hooks such as `lakefs_commit` and `iceberg_snapshot_id` when they
  are available and relevant

## Shared-Library Ownership Model

| Library | Authoritative Contents | Primary Owner Role | Required Reviewers | Promotion Rule |
| --- | --- | --- | --- | --- |
| `libs/schemas` | canonical evidence models, provenance objects, review and sensitivity enums, validation logic | architecture lead | data and orchestration lead, BFF and API lead for cross-boundary changes | breaking changes require coordinated consumer review |
| `libs/contracts` | BFF request and response envelopes, service-to-service sync contracts, integration event payload schemas | BFF and API lead | architecture lead plus at least one consuming owner | any cross-boundary payload must be published here before reuse |
| `libs/policy` | sensitivity taxonomy, decision vocabulary, deny reasons, export/view distinction types, policy helpers | policy and security lead | architecture lead and affected consuming owner | deny-by-default behavior until restricted-role governance is formalized |
| `libs/prompts` | versioned prompt assets, prompt safety clauses, routing metadata | semantics or QA lead | policy and security lead | prompt changes require evaluation traceability |
| `libs/evaluation` | evaluation schemas, metrics helpers, regression thresholds, dataset descriptors | evaluation and release lead | affected workflow owner | release-impacting thresholds require documented evidence |

## Contract Versioning And Compatibility Rules

- Shared contract surfaces use semantic versioning.
- `major` means a breaking schema or semantic change.
- `minor` means an additive backward-compatible change.
- `patch` means a non-semantic correction, documentation clarification, or
  backward-compatible metadata fix.
- Existing enum values may be deprecated but may not be repurposed.
- Removing a required field, changing field meaning, or changing policy meaning
  is a breaking change.
- Event producers may add optional fields within the same major version, and
  consumers must ignore unknown optional fields within that major version.
- If an event meaning changes materially, publish a new major contract version
  and, when necessary, a new event type rather than mutating the meaning of the
  old one in place.
- A producer-side contract change is incomplete until declared first-party
  consumers are validated against it.
- `docs/implementation` remains the human-readable source of intent,
  `libs/schemas` and `libs/contracts` are the executable contract sources, and
  generated client artifacts are derived from those sources rather than
  authoritative in their own right.

## References

- `Architecture_Plan.md`, sections 2, 3, 4, and Part II section 3
- `pm/01_architecture_constraints.md`
- `pm/14_artifact_inventory.md`
- `pm/16_decision_boundaries.md`
