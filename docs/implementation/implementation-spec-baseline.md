# MapTheIsland Implementation Specification Baseline

## Purpose

This document is the Phase 00 implementation baseline for the MapTheIsland
repository. It converts the architecture from narrative guidance into an
execution-ready baseline for repository structure, service boundaries, contract
ownership, shared schema publication, and quality enforcement.

It is intentionally conservative. Where the architecture leaves a production
detail unresolved, this document records the unresolved detail explicitly
instead of inventing hidden scope or unstated operational assumptions.

## Phase 00 Coverage

This baseline directly supports these Phase 00 deliverables:

- `P00-T01`: implementation-spec outline, traceability baseline, and explicit
  gap register
- `P00-T02`: canonical evidence schema baseline, provenance tuple baseline, and
  schema publication strategy
- `P00-T03`: policy taxonomy, role/export baseline, prohibited-flow catalog,
  and policy verification matrix
- `P00-T04`: initial service catalog and contract boundary baseline
- `P00-T05`: repository structure, testing, and engineering standard baseline

## Governing Constraints

The following architecture constraints are directly operationalized here:

- `AC-03` Evidence Before Inference
- `AC-04` Mandatory Provenance
- `AC-05` Layer Separation
- `AC-07` Human Adjudication For High-Impact Actions
- `AC-08` QA Abstention
- `AC-09` Browser Is Untrusted For Privileged Access
- `AC-10` Policy Before Higher-Level NLP
- `AC-16` Versioned Derived Assets
- `AC-17` Test And Evaluation Gates Are Release Blockers
- `AC-18` Implementation Must Remain Inspectable

## Repository Baseline

The repository will follow the architecture's platform-oriented monorepo model.
The initial top-level structure is:

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
/docs
  /implementation
```

The current implementation slice only materializes the root documentation,
frontend workspace baseline, the shared schema, contract, and policy packages,
the repository CI baseline, the first provider-neutral infrastructure
scaffolding, and the internal-only local self-managed development target. The
remaining service directories stay reserved but unimplemented until the
service-boundary and platform tasks are further advanced.

## Service Catalog Baseline

The service catalog summary below defines the initial ownership intent and first
implementation phase for each architecture-named service. The authoritative
`P00-T04` service, API, event, and versioning rules now live in
`docs/implementation/service-boundaries-and-contracts.md`.

| Service | Primary Responsibility | Primary Owner Role | First Delivery Phase | Primary Inputs | Primary Outputs |
| --- | --- | --- | --- | --- | --- |
| `harvester` | discover official DOJ source material and track incremental changes | document processing lead | `P02` | seed URLs, prior manifests | source discovery events, fetch jobs |
| `docproc` | route files, parse PDFs, preserve native text and layout evidence | document processing lead | `P02` | raw evidence objects, manifests | page assets, text candidates, layout assets |
| `ocr` | recover text from image-only or low-confidence pages | document processing lead | `P02` | page images, OCR jobs | OCR text outputs, confidence metrics |
| `extractor` | emit entities, aliases, relations, claims, and event candidates | semantics or NLP lead | `P04` | canonical spans, policy-safe text | semantic candidates with provenance |
| `resolver` | perform identity resolution and merge-review preparation | semantics or NLP lead | `P04` | entity and alias candidates | canonical entities, merge candidates |
| `topics` | generate topic, sense, and weak-label research artifacts | retrieval, graph, and analytics lead | `P05` | policy-safe semantic assets | topic artifacts, weak labels, evaluations |
| `graph-builder` | materialize event-centric graph projections | retrieval, graph, and analytics lead | `P05` | canonical entities, claims, events | Neo4j graph projections |
| `indexer` | build retrieval artifacts and OpenSearch indices | retrieval, graph, and analytics lead | `P05` | accepted evidence and semantics | retrieval artifacts, search indices |
| `review-api` | manage review queues, adjudications, and audit events | review operations lead | `P03` | review items, policy context | adjudications, invalidation events |
| `qa-orchestrator` | assemble evidence packs, enforce support verification, and mediate QA | BFF and API lead with policy/security lead | `P07` | policy-safe retrieval outputs | QA evidence packs, answer artifacts, abstentions |
| `bff` | mediate browser requests to trusted backends and enforce policy context | BFF and API lead | `P06` | analyst requests, tokens, downstream data services | UI response envelopes with provenance and policy context |

## Policy Baseline

The detailed `P00-T03` policy baseline now lives in
`docs/implementation/policy-taxonomy-and-safety-model.md`. That document fixes:

- the authoritative implementation meaning of each sensitivity enum value
- provisional role and export intent pending `OQ-03`
- prohibited flows that must become negative tests later
- the minimum verification obligations for Phase 03 through Phase 07

## Shared Library Baseline

The architecture requires shared contract surfaces so services and the web
application do not drift into incompatible, inferred interfaces. The library
baseline is:

| Library | Responsibility | Initial Phase 00 Status |
| --- | --- | --- |
| `libs/schemas` | canonical evidence models, provenance tuple, enums, and validation logic | implemented in this slice |
| `libs/contracts` | shared OpenAPI fragments, response envelopes, and async event payloads | executable Phase 01 baseline now published for service catalog, operational endpoints, and async event envelopes |
| `libs/policy` | sensitivity taxonomy, policy helpers, and denied-flow constants | executable Phase 01 baseline now published for deny-by-default role, sensitivity, and prohibited-flow vocabulary |
| `libs/prompts` | versioned prompt templates and QA prompt safety assets | reserved for later model-assisted phases |
| `libs/evaluation` | evaluation datasets, metrics helpers, and threshold baselines | reserved for `P05` and `P07` |

## Canonical Schema Baseline

The first concrete shared contract is the evidence schema package under
`libs/schemas`. Its immediate responsibilities are:

- define `Document`, `Page`, `Span`, and `Claim`
- define the mandatory provenance tuple as a first-class reusable object
- define versioned enums for sensitivity and review state
- reject invalid records early through explicit validation
- keep derived artifacts tethered to evidence-layer provenance

This package is the repository's first executable expression of the
architecture's evidence-first model. It is intentionally small enough to reach
100 percent coverage immediately.

## Contract Publication Strategy

The repository now publishes contracts in three layers:

1. Human-readable implementation documents under `docs/implementation`
2. Executable Python schemas under `libs/schemas`
3. Executable shared-library contracts under `libs/contracts` and
   `libs/policy`, with later route-specific BFF and UI payloads extending those
   baselines

Until frontend and BFF runtime code exists, the Python shared-library layer is
the authoritative executable contract source. When TypeScript clients arrive,
generated or manually mirrored types must remain version-locked to the
published schema and policy baselines rather than recreated from memory.

Detailed ownership, API, event, and compatibility rules now live in
`docs/implementation/service-boundaries-and-contracts.md`.

## Testing And Documentation Enforcement

The repository baseline enforces the following rules immediately:

- handwritten code must remain at 100 percent coverage
- local automated tests must pass at 100 percent
- integration tests must pass at 100 percent once applicable code exists
- non-trivial modules, public models, validators, and helper functions require
  docstrings
- non-obvious algorithmic or validation behavior requires inline rationale
  comments
- Python bootstrap is normalized through `uv`, and `uv.lock` is required
- frontend dependency bootstrap is normalized through `pnpm`, and
  `pnpm-lock.yaml` is required once dependencies are installed

The root Python configuration therefore prioritizes test tooling, coverage
thresholds, Ruff, and mypy before feature-scale service code is added. The
authoritative engineering rules now live in
`docs/implementation/engineering-standards-baseline.md`.

## Initial Implementation Order

With the Phase 00 baseline published and the first shared-library and CI slices
complete, the current execution order is:

1. use the published Phase 00 policy, contract, and engineering baselines as
   the authoritative inputs for Phase 01 work
2. keep the shared-library package-boundary transition from `P01-T01` stable as
   later phases add service runtimes and downstream consumers
3. continue provider-neutral `P01-T02` to fix Terraform and Helm structure,
   naming intent, storage intent, and cluster-baseline contracts without
   assuming a hosting provider
4. narrow `OQ-01` and the safe local portion of `OQ-02` into an internal-only
   local self-managed dev target so Phase 01 can validate cluster bootstrap
   behavior without making higher-environment claims
5. keep `P01-T06` observability and runtime-bootstrap follow-on work blocked
   behind `P01-T04-S04`
6. begin provider-specific `P01-T03` only after the deployment environment is
   narrowed enough to avoid unsafe assumptions

## Explicitly Deferred Items

The following items are intentionally not invented in this document:

- production node sizing and budget-specific scaling targets
- final secret-management wiring details beyond the architecture-selected tool
  classes
- final BFF route schemas and event payloads
- final staging, pilot, or production dataset composition
- final restricted-role governance approvals

Those details are tracked in the PM open-question surfaces and the implementation
gap register.
