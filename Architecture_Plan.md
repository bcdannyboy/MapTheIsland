Below is a concrete reference architecture for a provenance-first Epstein-files analysis platform. It is designed for the public DOJ corpus as it exists now: the department says the library is still updateable if additional documents are identified, the current production totals nearly 3.5 million released pages plus more than 2,000 videos and 180,000 images, DOJ warns that search can be unreliable for some formats such as handwritten material, and its production memorandum says some emails may display differently, appear cut off, or contain symbols because of source-format differences. Those facts rule out a simple “dump it in a vector DB” design. The system has to be multimodal, versioned, provenance-centric, and explicit about uncertainty. ([Department of Justice][1])

It also has to be victim-protective by construction. DOJ’s review protocol was centered on redacting victim-identifying information, applying multiple review layers, and handling sexually explicit materials in redacted form; the architecture therefore cannot treat redactions as puzzles to solve, cannot expose protected adjacency context by default, and cannot turn model hypotheses into person-level accusations. LLMs in this design are annotation and synthesis tools, not evidentiary authorities. ([Department of Justice][2])

# Part I — Ingestion and analysis

## 1. Scope, explicit assumptions, and architectural invariants

This reference implementation fixes the hidden assumptions up front.

1. The source corpus is limited to lawfully released public material plus metadata you generate from that material.
2. The system never attempts to deanonymize redactions or infer victim identities.
3. The primary truth object is an evidence-backed span, not a topic label, embedding, or LLM summary.
4. Every derived artifact must carry provenance: source document ID, page, coordinates or offsets, extractor version, model version, timestamp, and review state.
5. The system separates four layers: raw evidence, extracted claims, inferred hypotheses, and user interaction.
6. Risk scoring is applied to passages, events, and document clusters, never directly to people.
7. Human adjudication is required for high-impact merges, sensitive labels, and policy-sensitive exports.
8. The QA layer must abstain when support is weak or policy blocks the request.

That structure is not optional. It is the minimum needed for a corpus whose official search is incomplete for some formats and whose production involved complex manual review and redaction procedures. ([Department of Justice][3])

## 2. Reference deployment and control plane

The deployment target is a self-managed Kubernetes cluster, because the platform has a clear split between stateless services and stateful services, and Kubernetes gives you the right primitives for both. Stateless services run as Deployments. Stateful services such as PostgreSQL, Kafka, OpenSearch, and Neo4j run as StatefulSets with persistent volumes. Helm packages the platform services and third-party dependencies. Terraform provisions the cluster, networking, storage classes, object buckets, DNS, and IAM. Argo CD continuously reconciles the cluster from Git so that deployment is declarative and auditable. cert-manager issues and renews TLS certificates for internal and external endpoints. ([Kubernetes][4])

The cluster should be split into three node pools. The first is a general CPU pool for APIs, orchestration, search indexing, and lightweight NLP. The second is a stateful SSD-backed pool for databases and brokers. The third is a GPU pool for OCR recovery, embedding generation, reranking experiments, and self-hosted model serving. This is a single-region reference deployment with off-cluster backups and immutable object storage; multi-region disaster recovery is possible, but the reference design keeps one writer region for analytical assets so that provenance and snapshot lineage stay simple and deterministic.

A clean repository layout matters because this is not one application; it is a platform. The monorepo should look like this:

```text
/infra
  /terraform
  /helm
/services
  /harvester
  /docproc
  /ocr
  /extractor
  /resolver
  /topics
  /graph-builder
  /indexer
  /review-api
  /qa-orchestrator
  /bff
/apps
  /web
/libs
  /contracts
  /prompts
  /schemas
  /policy
  /evaluation
```

Python services are managed with `uv`, which is a modern Python project and package manager. The frontend workspace is managed with `pnpm`, which has built-in workspace support for monorepos. Python code is linted and formatted with Ruff, statically typed with mypy, and tested with pytest. Browser-level end-to-end tests are written in Playwright. These are not cosmetic choices; they give you lockfiles, reproducible builds, static contracts, and a single CI surface for a platform with many cooperating services. ([Astral Docs][5])

Secrets do not live in environment files committed to Git. Vault is the system of record for secrets, keys, and short-lived credentials. External Secrets Operator synchronizes the necessary material into Kubernetes namespaces. Kubernetes Secrets exist only as delivery vehicles inside the cluster and should be encrypted at rest. This arrangement matters because the platform contains database credentials, model API keys, storage credentials, and signing keys for signed object URLs. ([HashiCorp Developer][6])

## 3. Storage architecture and system-of-record choices

The storage layer is deliberately plural. A forensic corpus platform needs different databases for different workloads, and collapsing them into one system usually destroys either provenance, queryability, or performance.

The raw evidence layer lives in S3-compatible object storage behind the S3 API. On AWS that is Amazon S3. On-premises it can be MinIO or another tested S3-compatible store. lakeFS sits in front of that storage and provides Git-like data version control semantics over the object store, including branching and merging of data states. That is the correct tool for ingest batches, reprocessing branches, and analyst-safe experimental transformations. ([AWS Documentation][7])

Structured analytical assets are stored in Apache Iceberg tables on object storage. Iceberg gives you snapshots, atomic table-state updates, schema evolution, hidden partitioning, and time-travel-oriented table semantics. In the reference implementation, the Iceberg catalog is the JDBC catalog backed by PostgreSQL, because it keeps the control plane smaller and relies on PostgreSQL’s transactional guarantees. Trino supports the Iceberg JDBC metadata catalog directly, although its documentation notes that the JDBC catalog can have future compatibility issues if Iceberg introduces breaking changes; if multi-engine catalog evolution becomes a first-order requirement later, switch the catalog to Iceberg REST without changing the rest of the data model. ([Apache Iceberg][8])

PostgreSQL is the operational metadata database. It stores document manifests, job states, review tasks, adjudications, identity mappings, API audit logs, prompt logs, and compact structured objects that do not belong in the search index or graph store. JSONB is used heavily for semi-structured extractor payloads and provenance payloads. Row-level security is enabled on policy-sensitive tables so that downstream consumers cannot accidentally bypass role filtering. `pgvector` is enabled, but only for small operational embedding workloads such as entity cards, QA evaluations, and review suggestions; it is not the primary corpus retrieval engine. ([postgresql.org][9])

OpenSearch is the retrieval layer. It is the right primary search engine because it already supports lexical search, neural/semantic search, and hybrid search pipelines that normalize and combine scores. It also supports document-level security. An important operational detail from the docs: OpenSearch DLS restricts reads, not writes. That means every write path must remain behind trusted services and service accounts; you do not rely on DLS to protect write operations. ([OpenSearch Docs][10])

Neo4j is the graph system. It stores the canonical property graph for people, aliases, contact points, documents, spans, events, topics, redactions, and evidence claims. Cypher is the query language. The Graph Data Science library provides centrality, community detection, similarity, path finding, node embeddings, and topological link prediction algorithms. Neo4j’s RBAC model gives you another enforcement point for least-privilege graph access. ([Neo4j Graph Intelligence Platform][11])

Trino is the interactive SQL engine over Iceberg and operational sources. It queries Iceberg directly, supports S3-backed lakehouse data, and also has a PostgreSQL connector. That makes it the right engine for saved analytical queries, heatmaps, investigator dashboards, and offline analyst notebooks that need SQL over large derived tables without shipping everything through application code. Trino also has an OPA access-control plugin, which is useful when you need catalog-level authorization to line up with the rest of the policy model. ([trino.io][12])

The shortest accurate description of the data plane is this:

```text
S3-compatible object store + lakeFS  = immutable/versioned evidence
Iceberg on object storage            = analytical assets
PostgreSQL                           = operational metadata and adjudication
OpenSearch                           = retrieval and hybrid search
Neo4j                                = graph reasoning and relationship analysis
Trino                                = ad hoc SQL over derived assets
```

## 4. Orchestration, eventing, and model-serving control

Dagster is the orchestration layer because its software-defined asset model maps directly onto the architecture. Each durable artifact in the platform is treated as an asset: raw manifest, parsed pages, canonical spans, resolved entities, events, topics, graph projections, search indexes, and UI aggregates. Dagster then gives you materialization tracking, dependencies, lineage, partitioning, and scheduled or sensor-driven updates. That is a better fit than step-centric orchestration because the output assets are the objects that matter to analysts and to downstream QA. ([Dagster Docs][13])

Kafka is the event backbone. Every significant state change emits an event: file discovered, file downloaded, file parsed, OCR completed, claims extracted, entity merge proposed, adjudication accepted, index refreshed, graph projection rebuilt. Kafka is designed to store streams of events durably and to process them as they occur or retrospectively. Spark Structured Streaming consumes the event stream for incremental transformations and writes out new Iceberg assets. ([Apache Kafka][14])

Spark is not the whole application; it is the heavy transform engine for larger batches and stream/batch unification. Spark SQL provides the structured data-processing model, and Structured Streaming provides the scalable fault-tolerant incremental execution model for event-driven transformations. Small operational tasks stay in Python services. Large fan-out tasks—embedding generation, daily aggregates, topic retrains, graph feature backfills—move to Spark jobs. ([Apache Spark][15])

All LLM traffic is forced through a model gateway. The reference stack uses LiteLLM Proxy as the unified gateway and vLLM for self-hosted open-weight model serving. LiteLLM gives you a single compatible surface across providers and supports routing, fallbacks, and traffic controls. vLLM exposes an OpenAI-compatible server, which keeps client code stable across self-hosted and vendor endpoints. The browser never talks to a model directly. ([LiteLLM][16])

## 5. Source acquisition, evidence immutability, and provenance

The harvester service is responsible for discovering and re-discovering official source material. Its seed list is restricted to official DOJ library pages and associated official document URLs. The harvester stores the page URL, discovered timestamp, response headers, MIME type, byte length, SHA-256 hash, source class, and parent/child relationships. Because DOJ explicitly says the library can be updated if additional documents are identified, harvesting is incremental and idempotent rather than one-off. ([Department of Justice][1])

Each ingest batch runs on its own lakeFS branch named `ingest-<timestamp>`. All downloaded objects go to a `raw/` prefix keyed by SHA-256. Nothing in `raw/` is modified in place. If a file changes upstream, it is a new object, a new hash, and a new ingest event. On successful validation, the branch is merged into `main`. On failed validation, the branch is retained for audit but never merged. That gives you exact replayability for any answer later generated by the platform. ([docs.lakefs.io][17])

The provenance key is a tuple, not a single ID:

```text
(source_url, fetch_timestamp, sha256, lakefs_commit, iceberg_snapshot_id, extractor_version, model_version)
```

That tuple is carried into every downstream record. A claim without that tuple is not admitted into the system.

## 6. File triage, deduplication, and routing

Every object first goes through exact and near-duplicate analysis. Exact duplicates are identified by SHA-256. Near duplicates are identified with SimHash or MinHash over normalized text plus TLSH or ssdeep over the byte stream; duplicates are never deleted, only grouped into a duplicate set with one canonical representative and provenance edges to all source copies. This matters because the DOJ corpus itself was over-collected and then deduplicated during production, and duplicative exhibits across investigations are expected. ([Department of Justice][18])

Routing uses content detection by magic bytes and MIME, not file extension. The first classifier distinguishes: PDF, image, text, HTML, office document, archive, audio, video, and unknown binary. Archives are recursively exploded into child members, but the raw archive itself is still preserved as evidence. File routing is deterministic and logged in the `ingest_manifest` table.

The concrete Python libraries for the core routing layer are straightforward. `pypdf` is used for PDF structure, attachments, and native text extraction. PyMuPDF is used for block-level, word-level, rectangle-aware extraction and page rendering. `unstructured` is used for element partitioning and high-resolution document decomposition. `python-magic` does MIME detection. `ffmpeg` handles video and audio metadata extraction. `openpyxl` handles spreadsheets. For text normalizations and operational transforms, use `orjson`, `pandas`, `polars`, and `pyarrow`; when the transform becomes large or distributed, push it into Spark. `pypdf`, PyMuPDF, and Unstructured are the non-negotiable core document-processing libraries in the reference implementation. ([pypdf.readthedocs.io][19])

## 7. PDF, image, and layout processing

The PDF lane runs in four ordered passes.

Pass one is structural parse with `pypdf`. It extracts metadata, page count, embedded attachments, encryption state, and any immediately readable text. Pass two is geometric extraction with PyMuPDF, which produces blocks, words, images, and page coordinates and can extract text in reading order or from rectangles. Pass three is semantic partitioning with Unstructured: `partition_pdf(strategy="fast")` for good native-text PDFs and `partition_pdf(strategy="hi_res", infer_table_structure=True)` when layout fidelity matters. Pass four is OCR recovery for pages whose native text is missing or unreliable. ([pypdf.readthedocs.io][19])

The OCR lane is tiered. Tesseract is the baseline OCR engine for machine-printed text and low-cost batch recovery. docTR is the deep-learning OCR fallback for hard printed layouts and low-quality scans because it uses a two-stage detect-then-recognize approach. TrOCR is the handwriting-oriented fallback for end-to-end transformer OCR when a handwriting classifier or confidence heuristics indicate the page is not standard print. The lane is explicit: Tesseract first, docTR when printed OCR quality is poor, TrOCR when handwriting probability is high, and human review when confidence remains below threshold. ([GitHub][20])

Because DOJ warns that official search can be unreliable for handwritten or technically difficult materials, and because its own production memo says certain emails can render badly or appear cut off, the platform preserves three synchronized layers for every page: the page image, the native extracted text, and the OCR text. The UI later lets analysts toggle among those layers instead of pretending there is one canonical text rendering when the source itself does not justify that certainty. ([Department of Justice][3])

The routing thresholds are fixed as defaults, not guessed implicitly. In the reference implementation, a PDF page stays on the native-text lane only if median visible extracted characters per page is at least 300, the control-character ratio is below 3 percent, and native text covers at least 70 percent of detected text blocks. Otherwise it goes to `hi_res` partitioning. If OCR median confidence is below 0.92, or the page is classified as likely handwritten, it moves to the fallback OCR lane and is tagged `needs_review`. Those numbers are starting operating thresholds; they are re-estimated after you build a gold set.

## 8. Canonical evidence model

The atomic unit is the span. Not page. Not document. Not chunk.

A minimal canonical schema is:

```text
Document(
  document_id, source_url, sha256, mime_type, doc_type, page_count,
  lakefs_commit, ingest_batch_id, sensitivity, review_state, metadata_json
)

Page(
  page_id, document_id, page_number, image_uri, width, height,
  native_text_confidence, ocr_confidence, handwriting_prob, layout_json_uri
)

Span(
  span_id, page_id, block_type, text_raw, text_normalized,
  char_start, char_end, bbox, extraction_engine, confidence,
  sensitivity, review_state, checksum
)

Claim(
  claim_id, subject_ref, predicate, object_ref_or_literal,
  time_start, time_end, location_ref, source_span_id,
  extractor, model_version, confidence, review_state
)
```

That schema is written to Iceberg for analytical access and mirrored in PostgreSQL for operational point lookups. The canonical `Span` record must also store extractor identity such as `pypdf`, `pymupdf`, `unstructured`, `tesseract`, `doctr`, or `trocr`. Without that, later QA cannot tell whether a disagreement is substantive or just an OCR artifact.

For programmatic reads of Iceberg assets from Python services that do not need Spark, use `pyiceberg`. For high-throughput SQL reads, use Trino. For point reads and transactions, use PostgreSQL. That split is intentional. ([py.iceberg.apache.org][21])

## 9. Sensitivity tagging and policy labeling

Before any high-level NLP happens, the platform runs a sensitivity pass. This pass does not decide what is “true.” It decides what is safe to expose, embed, summarize, or send to a model.

The first layer uses deterministic recognizers and Presidio. Presidio is built specifically for detecting PII in text and can be extended with custom recognizers, including language-model-based recognizers. In this platform it is used for emails, phone numbers, physical addresses, URLs, IDs, and explicit protected classes you define in custom recognizers. Presidio is advisory, not sufficient by itself, so the platform combines it with rule-based redaction geometry, victim-name allow/deny lists maintained under policy, and source-specific heuristics. ([Microsoft GitHub][22])

The second layer assigns a sensitivity enum at the span level: `public_general`, `public_explicit_redacted`, `restricted_redaction_context`, `protected_victim_context`, `withheld_source_gap`, and `unsafe_for_llm`. Only spans not tagged `unsafe_for_llm` can be sent into synthesis prompts. Restricted spans can still exist in the evidence store but are excluded from general search indices and from broad QA flows.

## 10. Entity extraction, aliasing, and identity resolution

Entity extraction is two-track: deterministic first, learned second.

The deterministic track extracts email addresses, URLs, domains, phone numbers, dates, times, monetary values, and common structured identifiers. That is done with explicit parsers and regexes because these fields do not benefit from a generative model. The learned track extracts people, organizations, locations, roles, aliases, nicknames, and named objects using spaCy pipelines and Hugging Face token-classification models fine-tuned for the corpus. spaCy provides a production-friendly NLP pipeline model and named-entity components. Hugging Face token classification is used for custom NER where the corpus vocabulary departs from generic newswire entities. ([spaCy][23])

Layout-aware extraction is not run everywhere. It is reserved for pages where geometric context changes interpretation, such as contact sheets, flight-log-like layouts, mixed handwritten/typed pages, forms, or annotated legal exhibits. For those pages, use LayoutLMv3-based inference or fine-tuning because it explicitly combines text and visual/layout information in a multimodal transformer. That capability is useful for layout-heavy evidence, but it should be a specialist lane, not the default lane, because plain text pages are cheaper and simpler to process with standard pipelines. ([Hugging Face][24])

Alias extraction is handled explicitly. The extractor scans for cues such as `aka`, `a/k/a`, quoted nicknames, email local parts, signature blocks, and repeated pairings of a formal name with a short form. Each extracted alias becomes an `AliasCandidate` tied to the source span. Nothing is merged into the canonical entity until it passes identity resolution.

Identity resolution uses a staged process. First, blocking rules generate candidate pairs based on normalized name tokens, shared contact points, shared domains, overlapping roles, or co-occurrence in the same thread. Second, a pairwise scorer combines string similarity, contact-point overlap, contextual embedding similarity, temporal compatibility, and document-provenance similarity. Third, a clustering stage forms canonical entity groups. Fourth, high-impact merges are reviewed by humans. This is the right place for `rapidfuzz`, feature-based gradient boosting, and compact transformer similarity models. The graph never treats an unreviewed merge as if it were settled fact.

## 11. Thread reconstruction, relation extraction, and event extraction

The system should not build a graph directly from entity co-occurrence. It should build it from events and claims.

Thread reconstruction is document-type specific. Printed or PDF-rendered emails are reconstructed from detected header fields (`From`, `To`, `CC`, `BCC`, `Date`, `Subject`), quote-block patterns, subject normalization (`Re:`, `Fwd:` stripping), attachment references, and visual indentation or separator rules. Because the DOJ production memo says emails may appear cut off or contain symbols depending on format, thread reconstruction always stores a confidence score and a `fragmentary_rendering` flag. Thread grouping is never hidden from the analyst as though it were perfect. ([Department of Justice][2])

Relation extraction turns spans into typed relations such as `sent_to`, `copied_to`, `mentions`, `located_at`, `contact_point_of`, `alias_of`, `requested`, `scheduled`, `traveled_to`, `attached_to`, and `near_redaction`. This stage uses schema-constrained extraction with Pydantic-validated JSON outputs and post-extraction validators. A relation without a valid subject type, predicate, object type, and source span is rejected.

Event extraction is the real backbone. The event ontology should minimally include `EmailEvent`, `TravelEvent`, `MeetingEvent`, `CallEvent`, `PaymentEvent`, `LegalFilingEvent`, `InterviewEvent`, `AttachmentEvent`, `RedactionEvent`, and `MediaEvidenceEvent`. Each event stores participants, time interval, location, supporting spans, and extraction confidence. A second pass performs cross-document event coreference so that multiple mentions of the same underlying real-world occurrence map to one canonical event with many evidence edges.

Temporal normalization is conservative. If the source says “Monday” and the document date is known, the system resolves it to an interval and marks the resolution method. If the source only implies a month or season, the event stores an uncertain interval. The event layer is what later lets you ask, “show me all travel-related communications involving X in the 30 days before Y,” without confusing mentions with actions.

## 12. Topic modeling, dynamic topics, and sense induction

Topic modeling is run by document family, not across the entire corpus indiscriminately. Emails, legal filings, interview transcripts, handwritten notes, logs, image captions, and spreadsheets each generate different noise patterns. The reference pipeline trains separate BERTopic models per document family and then aligns them in a higher-level topic namespace. BERTopic is a strong fit here because it combines transformer embeddings with c-TF-IDF and supports dynamic topic modeling and online/incremental updates. ([Maarten Gr.github][25])

The baseline topic process is explicit. First, normalize text and strip boilerplate. Second, compute embeddings with SentenceTransformers. Third, cluster with HDBSCAN or the BERTopic default configuration. Fourth, generate topic descriptors with c-TF-IDF. Fifth, label stable topics with controlled vocabularies when a human reviewer accepts the mapping. Sixth, compute monthly or quarterly topic-over-time series. Nothing is written as a “final topic truth” until it survives stability checks across reruns and sampling perturbations.

Sense induction for suspected coded language is a separate pipeline from topic modeling. The steps are: mine candidate terms by unusual frequency shifts, keyness, PMI, or burstiness; collect fixed-size context windows around each occurrence; embed each context; cluster contexts into sense candidates; summarize each cluster into a neutral descriptor; and surface the cluster to analyst review with exemplars. The system records “candidate sense clusters,” not decoded meanings. That distinction is essential.

## 13. Redaction mapping and redaction-safe analysis

Redactions are first-class objects.

A `Redaction` record stores document ID, page, bounding box, approximate length class, nearby non-protected text window hashes, section label, repeated-template signature, and whether the redaction overlaps a visually obvious black-box region, a missing OCR gap, or an inherited upstream redaction. The purpose is to understand the distribution and contextual placement of redactions, not to recover the hidden content.

This is one of the hardest places to keep the architecture honest. The platform may compute conceptual clusters such as “redactions frequently adjacent to victim statements,” “redactions concentrated in signature blocks,” or “redactions in explicit-media review notes.” It must not provide a workflow whose practical effect is deanonymization of protected persons. That guardrail follows directly from the DOJ production protocol, which repeatedly emphasizes victim-protective redaction and additional review for sensitive material. ([Department of Justice][2])

Operationally, that means three things. First, redaction-neighbor text is stored hashed or masked in broad-access indices. Second, exports of redaction adjacency are disabled for normal roles. Third, QA prompts never include protected redaction neighborhoods.

## 14. Weak supervision and the LLM “jury” layer

Your “jury grading” idea is viable only if the unit of judgment is narrowed and the label semantics are made explicit.

The correct unit is one of: span, event, or document cluster. The label set should be domain-specific and non-accusatory, for example: `sexual_content_mention`, `travel_logistics`, `payment_or_transfer`, `introduction_or_recruitment_language`, `concealment_or_cleanup_language`, `victim_identifying_risk`, `legal_response`, and `media_sensitivity`. The system does not emit a label like “person is illicit.” It emits a probabilistic signal attached to evidence units.

The implementation uses weak supervision. Labeling functions come from three sources: deterministic heuristics, narrow task classifiers, and LLM judges. Snorkel is used to combine those weak signals into a probabilistic label model. LLM judging is routed through LiteLLM so that multiple providers or multiple self-hosted models can be sampled through one gateway, and self-hosted open models can run behind vLLM. Each judgment stores model ID, prompt template version, temperature, reasoning mode flag, raw verdict, normalized verdict, and latency/cost telemetry. ([docs.snorkel.ai][26])

The calibration rule is strict. Sensitive labels are not trusted until they are compared against a human-reviewed gold set, their reliability is measured by class, and they are thresholded for precision rather than raw recall. Disagreement among the judges is surfaced as uncertainty, not averaged away.

## 15. Graph construction and temporal analytics

The canonical graph schema should contain these node types: `Document`, `Page`, `Span`, `Entity`, `Alias`, `ContactPoint`, `Event`, `Topic`, `Redaction`, `Claim`, and `Community`. The core edge types are `HAS_PAGE`, `HAS_SPAN`, `MENTIONS`, `ALIAS_OF`, `USES_CONTACT_POINT`, `PARTICIPATED_IN`, `SUPPORTED_BY`, `OCCURRED_AT`, `PRECEDES`, `ASSOCIATED_WITH_TOPIC`, `NEAR_REDACTION`, `DUPLICATE_OF`, and `CORROBORATES`. Evidence-backed edges and inferred edges live in different relationship types or carry an `evidence_class` property so that they are never visually or analytically conflated.

Use NetworkX for prototype analytics in notebooks and Neo4j GDS for production algorithms. The standard production graph metrics are: PageRank or degree-like importance on communication subgraphs, Louvain or related community detection on person-event projections, similarity algorithms on topic neighborhoods, shortest-path and k-hop path expansion for explainable relationship tracing, node embeddings for candidate link discovery, and topological link prediction for “show me likely missing connective tissue” analyst tasks. Neo4j GDS explicitly supports centrality, community detection, similarity, path finding, node embeddings, and link prediction categories. ([networkx.org][27])

Temporal analytics are built on event tables, not raw documents. Derived Iceberg tables such as `daily_event_counts`, `daily_topic_activity`, `entity_topic_activity`, `thread_response_lags`, and `cooccurrence_windows` drive the time-series layer. Optional research lanes can add changepoint detection (`ruptures`), self-exciting process models (`tick`), or lag analysis (`statsmodels`). Those outputs stay in the hypothesis layer. The architecture should explicitly refuse to market them as proof of causation.

## 16. Retrieval, embeddings, and corpus vectorization

Do not vectorize only raw chunks. Vectorize the right artifacts.

The reference implementation creates embeddings for at least eight artifact classes: `span_chunk`, `page_summary`, `thread_summary`, `entity_card`, `event_card`, `topic_card`, `community_card`, and `timeline_segment`. That matters because a broad question such as “what themes intensified around a specific time window?” should retrieve topic and timeline artifacts, not just arbitrary 800-token chunks.

SentenceTransformers is the bi-encoder layer for embeddings and efficient semantic retrieval. CrossEncoder models from the same ecosystem are used as second-stage rerankers over the top-k candidates because that is exactly the retrieve-then-rerank pattern the library documents. OpenSearch hybrid search combines lexical and semantic retrieval in one result set. In practice the retrieval stack is: OpenSearch BM25 plus vector retrieval, then metadata filters, then graph expansion, then CrossEncoder rerank, then evidence-pack assembly. ([SentenceTransformers][28])

`pgvector` is still useful, but not as the main corpus engine. Use it for operational side features where you need vector similarity tightly joined with transactional metadata inside PostgreSQL, such as “show similar unresolved entity cards” or “find prior review cases similar to this OCR failure.” For primary document retrieval at corpus scale, OpenSearch remains the front door. ([GitHub][29])

A critical design rule follows from this: summaries and vector artifacts are derived objects with provenance, not evidence. They are stored in separate indices, versioned, and refreshable. When an upstream entity merge changes, every dependent artifact is rematerialized by Dagster, not patched ad hoc.

## 17. Validation, evaluation, lineage, and observability

Great Expectations is used for data validation at asset boundaries. Every important asset gets a checkpoint: manifest uniqueness, document row counts, page count consistency, schema conformance, null expectations for required provenance fields, and acceptable-value constraints for enums like `review_state` and `sensitivity`. Validation results are published as internal Data Docs. ([Great Expectations][30])

MLflow tracks model runs, prompt versions, extractor metrics, and evaluation outputs. It is used not just for model training but for corpus-specific extraction experiments: OCR model comparisons, entity-resolution threshold sweeps, reranker A/B runs, topic-model stability experiments, and QA support-rate evaluations. ([MLflow AI Platform][31])

Observability is end to end. OpenTelemetry instruments the services and sends traces, metrics, and logs through the OpenTelemetry Collector. Prometheus scrapes service metrics and query latencies. Grafana renders dashboards and alerting views. The platform should monitor at least: ingest lag, OCR queue depth, extraction success rate, entity-merge conflict rate, search latency percentiles, QA abstention rate, citation support rate, and policy-denied request counts. ([OpenTelemetry][32])

Lineage comes from three layers combined: Dagster asset lineage, lakeFS commit lineage, and Iceberg snapshot lineage. That combination lets you answer the operationally decisive question: “Which raw files, at which ingest state, using which extractor version, produced this exact derived claim or search index entry?” ([Dagster Docs][13])

## 18. Security and access control inside the analysis layer

Authentication is handled by Keycloak as the OpenID Connect provider. Authorization is split between application-level policy and datastore-level enforcement. OPA is the policy engine for fine-grained decisions. PostgreSQL uses row-level security for operational tables. OpenSearch uses document-level security for read filtering. Neo4j uses RBAC. Trino can delegate catalog access decisions to OPA. This is intentional defense in depth: one control plane policy, several datastore enforcement points. ([Keycloak][33])

The access model should define at least four roles. `reviewer_public` can read general public evidence and normal analytics. `reviewer_sensitive` can access policy-approved restricted contexts. `analyst_admin` can manage adjudications, merges, and exports. `system_service` is for internal services only. No human role gets broad write access to OpenSearch or the raw evidence store.

## 19. End-to-end processing sequence

The exact end-to-end flow is:

1. Harvester discovers a source URL.
2. Downloader fetches it, computes SHA-256, writes raw bytes to the S3/lakeFS raw prefix.
3. Manifest asset is materialized in Iceberg and PostgreSQL.
4. Dedup worker assigns exact and near-duplicate groups.
5. Router classifies file type by MIME and magic bytes.
6. Parser runs `pypdf` and PyMuPDF on PDFs.
7. Layout partitioner runs Unstructured.
8. OCR worker runs Tesseract, then docTR or TrOCR if required.
9. Canonical page and span assets are materialized.
10. Sensitivity pass tags spans and masks protected ones for broad indices.
11. Entity extractor emits candidates.
12. Relation extractor emits typed relations.
13. Event extractor emits event candidates.
14. Resolver merges aliases and entities.
15. Topic pipeline builds per-family topics and time slices.
16. Redaction mapper emits redaction objects and clusters.
17. Weak-supervision layer emits probabilistic signals on spans/events.
18. Graph builder writes the property graph to Neo4j.
19. Indexer writes retrieval artifacts to OpenSearch and operational vectors to PostgreSQL/pgvector.
20. Validation checkpoints run.
21. Human-review tasks are created for low-confidence or high-impact items.
22. On acceptance, the ingest branch is merged and new snapshots become visible to the UI.
23. QA and analytics surfaces query only the approved assets.

That is the baseline pipeline. Everything else is refinement.

# Part II — Data visualization and interaction with a web UI

## 1. UI philosophy and boundary conditions

The web application is not a chat shell with some charts attached. It is an evidence workbench. The primary interface objects are documents, pages, spans, entities, events, timelines, topics, graph neighborhoods, review queues, and cited answers. Chat exists, but only as one surface among many.

The browser sees only policy-filtered views. It never receives raw database credentials, never queries OpenSearch directly, never queries Neo4j directly, and never calls model providers directly. All privileged data access goes through a backend-for-frontend layer that enforces identity, role, policy, and query budgets.

## 2. Frontend stack and application shell

The frontend uses Next.js App Router with React and TypeScript. Next.js App Router gives you a file-system-based router and route-level code splitting. The UI uses TanStack Query for server-state fetching, caching, background refresh, and cache invalidation. Those are the correct primitives for a UI that has many data views, long-lived filters, and asynchronous jobs. ([Next.js][34])

The document viewer uses PDF.js because it is a standards-based PDF rendering library for the browser. The network/relationship explorer uses Cytoscape.js because it is specifically a graph theory library for analysis and visualization. Timeline, heatmap, streamgraph, chord, matrix, and custom analytical charts use Apache ECharts because it provides many chart types and supports custom series and progressive rendering for large data. ([Mozilla GitHub Pages][35])

The concrete frontend library list is:

```text
next
react
typescript
@tanstack/react-query
pdfjs-dist
cytoscape
echarts
zod
react-hook-form
```

`zod` and `react-hook-form` are useful for strict UI-side validation of filters, saved searches, and review forms, but the authoritative contracts still live on the backend.

## 3. Backend-for-frontend and service APIs

The backend-for-frontend is a FastAPI service. FastAPI is chosen because it gives you async endpoints, dependency-injected request handling, strong Python typing, and automatic OpenAPI documentation. In this system it is not a generic CRUD API. It is an orchestration layer that turns one analyst action into the minimum number of safe downstream queries across PostgreSQL, OpenSearch, Neo4j, Trino, and the model gateway. ([FastAPI][36])

The BFF exposes these core endpoints:

```text
GET  /search
GET  /documents/{document_id}
GET  /documents/{document_id}/pages/{page_number}
GET  /entities/{entity_id}
GET  /events/{event_id}
GET  /topics/{topic_id}
GET  /graph/subgraph
GET  /analytics/timeseries
GET  /analytics/heatmap
POST /qa/ask
POST /review/adjudications
POST /review/entity-merges
GET  /jobs/{job_id}
GET  /exports/{export_id}
```

Every endpoint returns a `policy_context`, `provenance_summary`, and `result_confidence` field where relevant. The frontend does not infer those on its own.

## 4. UI information architecture

The top-level routes are:

```text
/search
/documents/[documentId]
/entities/[entityId]
/events/[eventId]
/topics/[topicId]
/graph
/timeline
/review
/qa
/admin
```

Each route has a stable URL state model so that analyst work can be bookmarked, exported, or cited in notes. Filters such as date range, source family, document type, sensitivity, and confidence thresholds live in the URL query string and in saved searches.

## 5. Search surface

The `/search` route is the default entry point. It is a unified search page with result tabs for Documents, Entities, Events, Topics, Threads, and Redactions. The request flow is explicit: the BFF classifies the query, applies role-based filters, sends a hybrid lexical-plus-semantic query to OpenSearch, optionally expands the result set with graph neighbors from Neo4j, reranks the top candidates, and returns a grouped result object.

The UI shows why something matched. A result card exposes lexical hits, semantic score, graph-expansion reason, matching entities, date normalization, and number of supporting spans. Analysts can switch the ranking mode between `relevance`, `date_desc`, `support_count`, and `confidence`. Search is therefore not a black box. OpenSearch hybrid search and SentenceTransformers reranking do the retrieval work; the UI makes those mechanics inspectable rather than hidden. ([OpenSearch Docs][10])

## 6. Document viewer

The `/documents/[documentId]` route is the most important screen in the application. It is built around a PDF.js page viewer with overlay layers drawn from the canonical page model. Each page supports four synchronized overlays: native extracted text, OCR text, entities, and claims/events. Analysts can click a highlighted entity and see the supporting extracted spans, any competing OCR renderings, and the review state.

This view must include an extraction-mode toggle because the official library itself warns that some materials are not electronically searchable and the production memo describes rendering problems for some email formats. The UI therefore exposes `image layer`, `native text layer`, and `OCR layer` as first-class options. That is not a convenience feature; it is part of evidentiary honesty. ([Mozilla GitHub Pages][35])

A second panel on the right lists extracted objects on the current page: entities, relations, events, topics, and redactions. Every object has a confidence badge and a `jump to source` action. Redactions appear as objects, but their contextual visibility is policy-filtered. Users without the right role may see only the redaction box and abstract cluster label, not the protected neighborhood.

## 7. Entity dossier

The `/entities/[entityId]` route is a canonical dossier page. It has six sections: identity, aliases, contact points, evidence timeline, related events, and graph neighborhood. The page clearly distinguishes `canonical facts`, `candidate merges`, and `hypothesis-level associations`.

The identity section shows the canonical name, alias list, contact-point evidence, first/last seen dates, and confidence in the current resolution. The timeline section is built from event participation, not raw mentions, with raw-mention counts shown separately. The related-events section lists only events with supporting evidence. The graph neighborhood uses a server-generated subgraph, never the full global graph, because client-side rendering of the full corpus graph is analytically useless and operationally expensive.

## 8. Event explorer and timeline tools

The `/events/[eventId]` route is an evidence-backed event page. It shows participants, time interval, location, supporting spans, duplicate-event links, and an event-confidence explanation. Each event can be expanded into a local timeline showing the predecessor and successor events within a configurable temporal window.

The `/timeline` route is separate. It is a cross-entity, cross-topic explorer built on precomputed time-series tables. It supports: entity activity over time, topic intensity over time, event-type distributions, thread response lag histograms, and burst annotations. ECharts handles these views because it supports a broad set of chart types and custom series needed for interval bars, uncertainty bands, and density overlays. ([Apache ECharts][37])

Uncertainty is visible in the timeline. If an event time is a precise timestamp, it is shown as a point. If it is a date-only inference, it is shown as a thin interval. If it is a broad window, it is shown as a band. That keeps the UI aligned with the extraction model instead of falsely projecting exactness.

## 9. Topic atlas

The `/topics/[topicId]` route provides the topic atlas. It shows the topic label, descriptor terms, exemplar spans, related topics, temporal drift, associated entities, and evidence counts by document family. Because BERTopic supports dynamic topic views, the route can render how a topic’s descriptor terms and supporting exemplars shift over time. ([Maarten Gr.github][25])

The atlas has three analytic subviews. The first is a topic-over-time area or streamgraph. The second is an entity-topic matrix showing which canonical entities co-occur with the topic across time windows. The third is a context browser that lists exemplar spans from different document families so analysts can inspect whether a topic is semantically coherent or just an artifact of document boilerplate.

## 10. Graph explorer

The `/graph` route is a graph workbench, not a decorative network chart. Cytoscape.js renders server-materialized subgraphs only. The client never downloads the global graph. A typical query is “show 2 hops from entity X through events between date A and B, excluding raw co-mention edges.” The BFF turns that into a Cypher query plus policy filters, retrieves a bounded subgraph, and serializes it to Cytoscape elements.

The graph UI must visually differentiate edge classes. Evidence-backed edges are solid. Inferred edges are dashed. Duplicate relations are dotted. Restricted edges are hidden or summarized depending on role. Analysts can switch layouts, but the important choice is not the layout algorithm; it is the default edge filter. The default should exclude pure co-mention edges unless the user explicitly enables them. Cytoscape.js is the right rendering library here because it is built for graph analysis and visualization, but the graph semantics still have to be decided by the application. ([Cytoscape.js][38])

## 11. Redaction atlas

The redaction atlas is a restricted feature, not a default analyst landing page. It aggregates redactions by document family, section template, date band, and topic neighborhood. The UI exposes patterns such as “many short redactions in witness-statement headers” or “repeated medium-length redactions in travel-record summaries.” It does not provide raw adjacency export, bulk local-context download, or inverse-search tools that would make identity recovery easier.

The route exists because redactions are analytically meaningful objects in a heavily reviewed corpus. It is locked down because the review protocol was explicitly centered on protecting victims and other sensitive identities. ([Department of Justice][2])

## 12. QA workspace

The `/qa` route is a controlled analyst QA surface. It is not a general chatbot. The request path is:

1. Query classification.
2. Role/policy check.
3. Hybrid retrieval from OpenSearch.
4. Optional graph expansion from Neo4j.
5. CrossEncoder rerank.
6. Evidence-pack construction.
7. Prompt assembly with policy-based masking.
8. Model call through LiteLLM.
9. Support verification.
10. Citation rendering.

The answer card always carries a type label: `fact_lookup`, `timeline_reconstruction`, `relationship_trace`, `topic_synthesis`, or `hypothesis_summary`. It also carries one of three support states: `fully_supported`, `partially_supported`, or `insufficient_support`. If support is insufficient, the system abstains and shows the evidence pack instead of fabricating a narrative. The model gateway remains server-side and the answer composer never has access to unrestricted redaction context. ([LiteLLM][16])

The QA screen is most useful when it is inspectable. The lower half of the page should expose the evidence pack, the ranked sources, and the citation map. Clicking a citation jumps directly to the source page and highlighted span in the document viewer. That is how you make QA an analyst accelerator rather than a rumor engine.

## 13. Review workbench

The `/review` route is where model fallibility becomes operationally manageable. It has separate queues for OCR failures, low-confidence spans, entity-merge conflicts, unresolved aliases, event-coreference conflicts, sensitive-label adjudications, and QA support failures.

The workbench is keyboard-driven and optimized for high-volume expert review. Each queue item shows the original page image, extracted text variants, model output, confidence, and prior similar cases. Reviewers can accept, reject, split, merge, suppress, or escalate. Every adjudication writes to PostgreSQL, emits a Kafka event, and invalidates the affected downstream assets so Dagster can re-materialize only what changed.

This is where `pgvector` becomes useful operationally: it can suggest similar historical adjudications for the reviewer. This is also where MLflow and evaluation sets stay current, because accepted adjudications can be promoted into training or evaluation data.

## 14. Saved analytics and dashboard views

Not every question should go through QA. The platform therefore includes saved analytical views powered by Trino over Iceberg and PostgreSQL. The BFF exposes curated endpoints such as `/analytics/timeseries`, `/analytics/cooccurrence-matrix`, `/analytics/community-summary`, and `/analytics/review-throughput`. These are server-generated JSON responses, not raw SQL in the browser.

The point of Trino here is not convenience. It is to let you compute fast aggregates over large historical tables without bending the search index into an analytical warehouse. Trino queries Iceberg for wide scans and joins PostgreSQL for operational state when needed. Those outputs can then be cached by the BFF and served into ECharts views. ([trino.io][12])

## 15. Client-state, cache, and job management

TanStack Query manages server state. Every page-level query has a stable query key derived from route params and filter state. Background refetch keeps dashboards fresh without a full page reload. Long-running actions such as subgraph generation, export creation, or mass reindexing are modeled as jobs. The frontend polls `/jobs/{job_id}` with TanStack Query until completion and then invalidates dependent caches. ([TanStack][39])

This is preferable to browser-side websockets for the baseline system because the critical interaction pattern is analyst query plus eventual result, not high-frequency multiplayer editing. If collaborative review or presence features are later required, add a real-time channel then; it is not necessary in the first correct build.

## 16. UI security model

Login is handled by Keycloak with OIDC. The Next.js app receives only the minimum identity state it needs, while the FastAPI BFF validates tokens and resolves roles. OPA evaluates fine-grained policy, and downstream stores enforce their own reduced views: PostgreSQL via RLS, OpenSearch via DLS, Neo4j via RBAC, and Trino via OPA-backed or file-backed access control. ([Keycloak][33])

Three additional rules are critical. First, signed object URLs for page images and downloads are short-lived and scoped. Second, protected spans are never embedded into browser-local caches unless the user’s role explicitly permits it. Third, export policy is stricter than view policy: being allowed to see a summary does not automatically allow raw export of the supporting spans.

## 17. Testing, CI/CD, and release management

The backend test pyramid is: unit tests in pytest, contract tests against OpenAPI schemas, integration tests against ephemeral service containers, and evaluation regression tests for OCR, entity resolution, retrieval quality, and answer support. pytest is the base framework because its fixtures make complex integration setup manageable. ([pytest][40])

The frontend test pyramid is: component tests where appropriate, route-level smoke tests, and full end-to-end workflows in Playwright. Playwright is particularly useful here because the platform depends on document rendering, keyboard-heavy review flows, and navigation between linked evidence views. ([Playwright][41])

Delivery is GitOps. Helm charts define deployable units. Argo CD reconciles desired state from Git to the cluster. Terraform owns the underlying infrastructure. This is the right model for a platform where provenance and auditability matter operationally, not just for the corpus but for the software that processes it. ([Helm][42])

## 18. What this architecture is, and what it is not

This architecture is a concrete way to build a single coherent analytical system over the public corpus. It will produce a durable evidence layer, a structured claims layer, a temporal graph, a topic/sense/redaction analysis layer, and a policy-bounded QA interface. It is built from explicit, current technologies rather than a vague “use AI on the files” concept. ([Department of Justice][18])

It is not a one-store system. It is not a person-scoring system. It is not a redaction-recovery system. It is not a generic chatbot over PDFs. It is a forensic data platform whose organizing principle is: every downstream inference must remain tethered to inspectable evidence and explicit policy.

The next logical deliverable is a companion implementation spec: service-by-service API contracts, Iceberg table DDL, PostgreSQL schema, OpenSearch mappings, Cypher projections, and review-state workflows.

[1]: https://www.justice.gov/epstein?utm_source=chatgpt.com "Epstein Library | United States Department of Justice"
[2]: https://www.justice.gov/opa/media/1426091/dl "https://www.justice.gov/opa/media/1426091/dl"
[3]: https://www.justice.gov/epstein/search "https://www.justice.gov/epstein/search"
[4]: https://kubernetes.io/docs/home/ "https://kubernetes.io/docs/home/"
[5]: https://docs.astral.sh/uv/ "https://docs.astral.sh/uv/"
[6]: https://developer.hashicorp.com/vault/docs/about-vault/what-is-vault "https://developer.hashicorp.com/vault/docs/about-vault/what-is-vault"
[7]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"
[8]: https://iceberg.apache.org/spec/?utm_source=chatgpt.com "Spec - Apache Iceberg™"
[9]: https://www.postgresql.org/docs/current/datatype-json.html "https://www.postgresql.org/docs/current/datatype-json.html"
[10]: https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/?utm_source=chatgpt.com "Hybrid search - OpenSearch Documentation"
[11]: https://neo4j.com/docs/cypher-manual/current/introduction/ "https://neo4j.com/docs/cypher-manual/current/introduction/"
[12]: https://trino.io/docs/current/connector/iceberg.html "https://trino.io/docs/current/connector/iceberg.html"
[13]: https://docs.dagster.io/api/dagster/assets?utm_source=chatgpt.com "assets"
[14]: https://kafka.apache.org/documentation/ "https://kafka.apache.org/documentation/"
[15]: https://spark.apache.org/docs/latest/sql-programming-guide.html "https://spark.apache.org/docs/latest/sql-programming-guide.html"
[16]: https://docs.litellm.ai/docs/ "https://docs.litellm.ai/docs/"
[17]: https://docs.lakefs.io/ "https://docs.lakefs.io/"
[18]: https://www.justice.gov/opa/pr/department-justice-publishes-35-million-responsive-pages-compliance-epstein-files "https://www.justice.gov/opa/pr/department-justice-publishes-35-million-responsive-pages-compliance-epstein-files"
[19]: https://pypdf.readthedocs.io/en/stable/user/extract-text.html "https://pypdf.readthedocs.io/en/stable/user/extract-text.html"
[20]: https://github.com/tesseract-ocr/tesseract "https://github.com/tesseract-ocr/tesseract"
[21]: https://py.iceberg.apache.org/api/ "https://py.iceberg.apache.org/api/"
[22]: https://microsoft.github.io/presidio/?utm_source=chatgpt.com "Presidio: Data Protection and De-identification SDK"
[23]: https://spacy.io/ "https://spacy.io/"
[24]: https://huggingface.co/docs/transformers/model_doc/layoutlmv3 "https://huggingface.co/docs/transformers/model_doc/layoutlmv3"
[25]: https://maartengr.github.io/BERTopic/index.html "https://maartengr.github.io/BERTopic/index.html"
[26]: https://docs.snorkel.ai/docs/26.1/user-guide/evaluation/evaluation-overview/ "https://docs.snorkel.ai/docs/26.1/user-guide/evaluation/evaluation-overview/"
[27]: https://networkx.org/ "https://networkx.org/"
[28]: https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html "https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html"
[29]: https://github.com/pgvector/pgvector "https://github.com/pgvector/pgvector"
[30]: https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/ "https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/"
[31]: https://mlflow.org/docs/latest/ml/tracking/ "https://mlflow.org/docs/latest/ml/tracking/"
[32]: https://opentelemetry.io/docs/ "https://opentelemetry.io/docs/"
[33]: https://www.keycloak.org/securing-apps/oidc-layers "https://www.keycloak.org/securing-apps/oidc-layers"
[34]: https://nextjs.org/docs/app "https://nextjs.org/docs/app"
[35]: https://mozilla.github.io/pdf.js/ "https://mozilla.github.io/pdf.js/"
[36]: https://fastapi.tiangolo.com/ "https://fastapi.tiangolo.com/"
[37]: https://echarts.apache.org/ "https://echarts.apache.org/"
[38]: https://js.cytoscape.org/ "https://js.cytoscape.org/"
[39]: https://tanstack.com/query/latest "https://tanstack.com/query/latest"
[40]: https://docs.pytest.org/ "https://docs.pytest.org/"
[41]: https://playwright.dev/docs/intro "https://playwright.dev/docs/intro"
[42]: https://helm.sh/docs/ "https://helm.sh/docs/"

