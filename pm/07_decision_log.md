# Decision Log

Status values: `accepted`, `superseded`, `proposed`

## D-001: Evidence-Backed Span Is The Primary Truth Object

- Date: 2026-03-06
- Status: accepted
- Context: The architecture rejects topic labels, embeddings, and summaries as truth objects.
- Decision: The canonical evidence model will treat `Span` as the atomic evidentiary unit, with `Document`, `Page`, `Claim`, and downstream objects referencing spans.
- Consequences:
  - schema design centers on span provenance
  - UI and QA deep-link to spans
  - retrieval artifacts remain derived

## D-002: MapTheIsland Will Use A Plural Data Plane

- Date: 2026-03-06
- Status: accepted
- Context: the architecture assigns distinct responsibilities to object storage, Iceberg, PostgreSQL, OpenSearch, Neo4j, and Trino.
- Decision: The plan will not attempt to collapse evidence, search, graph, analytics, and operations into one datastore.
- Consequences:
  - more operational complexity
  - clearer system boundaries and better workload fit

## D-003: lakeFS Plus Object Storage Is The Evidence System Of Record

- Date: 2026-03-06
- Status: accepted
- Context: raw evidence must be immutable, branchable, and replayable.
- Decision: ingest batches will branch in lakeFS and merge only after validation.
- Consequences:
  - raw evidence replay is possible
  - downstream lineage can tie to ingest state

## D-004: Policy Enforcement Precedes Broad Semantic Promotion

- Date: 2026-03-06
- Status: accepted
- Context: restricted spans must not leak into broad search, prompts, or exports.
- Decision: sensitivity tagging, role policy, and review infrastructure are treated as a precondition for production semantic workflows.
- Consequences:
  - Phase 03 blocks unrestricted promotion of higher-level features
  - QA is delayed until policy-safe evidence packs exist

## D-005: Graph Construction Is Event-Centric

- Date: 2026-03-06
- Status: accepted
- Context: raw co-mention graphs would violate the architecture’s evidentiary standard.
- Decision: the canonical graph is built from claims, events, and explicit evidence classes; co-mention edges remain secondary and disabled by default in the UI.
- Consequences:
  - event extraction becomes a critical-path capability
  - graph explorer semantics are stricter but more defensible

## D-006: First Release Boundary Is The Evidence Workbench, Not QA

- Date: 2026-03-06
- Status: accepted
- Context: the architecture explicitly rejects a generic chatbot-over-PDFs release path.
- Decision: first release scope ends with a policy-safe evidence workbench including search, document viewer, entity/event views, review, and lineage.
- Consequences:
  - QA remains a later milestone
  - critical path favors evidence fidelity and review UX

## D-007: Browser Access Remains BFF-Mediated

- Date: 2026-03-06
- Status: accepted
- Context: the architecture states the browser never directly queries privileged stores or model providers.
- Decision: all browser-side data access will flow through a FastAPI BFF.
- Consequences:
  - BFF contract design is foundational
  - UI work depends on server-side orchestration models

## D-008: Derived Assets Are Re-Materialized, Not Manually Patched

- Date: 2026-03-06
- Status: accepted
- Context: upstream entity merges, review decisions, and policy changes can invalidate summaries, graph edges, and search artifacts.
- Decision: dependent assets will be rematerialized through orchestration and lineage, not manually edited.
- Consequences:
  - stronger operational discipline
  - more dependence on Dagster asset definitions and lineage

## D-009: PM Workspace Is Part Of The Product Delivery Surface

- Date: 2026-03-06
- Status: accepted
- Context: the user requested persistent project-management documentation for future sessions and subagents.
- Decision: `/pm` is treated as required operational infrastructure, not optional prose.
- Consequences:
  - future sessions must update planning artifacts as part of done criteria

## D-010: Test Pass Rate And Coverage Thresholds Are Hard Delivery Gates

- Date: 2026-03-06
- Status: accepted
- Context: the delivery model already required validation evidence, but implementation is now starting and the repository needs an unambiguous gating rule for task, phase, milestone, and release closure.
- Decision: all handwritten code in the repository must remain at 100 percent coverage, local automated tests must pass at 100 percent, and integration tests must pass at 100 percent before any task, phase, milestone, or release can be marked complete.
- Consequences:
  - coverage tooling must be established immediately and enforced continuously
  - new code cannot be merged without tests in the same change
  - completion evidence for every phase and milestone must include local test, integration test, and coverage reports
  - work must be split into smaller slices whenever a feature cannot land within the gate

## D-011: Phase 00 Shared Contracts Start As Executable Python Schemas

- Date: 2026-03-06
- Status: accepted
- Context: the implementation baseline needed a machine-validated contract source for `Document`, `Page`, `Span`, `Claim`, provenance, sensitivity, and review-state semantics before the BFF and web client exist.
- Decision: the first authoritative executable contract surface lives in `libs/schemas` as Pydantic models, with later BFF, event, and TypeScript contract surfaces required to align to that baseline rather than recreate it informally.
- Consequences:
  - Python services can reuse one strict schema package immediately
  - future TypeScript or OpenAPI publication work must remain traceable to the shared schema baseline
  - contract changes in `libs/schemas` become cross-workstream changes that require compatibility review

## D-012: Cross-Boundary Contracts Are Published Centrally And Versioned Semantically

- Date: 2026-03-06
- Status: accepted
- Context: `P00-T04` now requires a concrete rule for where browser-facing envelopes, service-to-service payloads, async event contracts, and shared policy vocabulary live, plus how those contracts evolve without silent consumer breakage.
- Decision: canonical evidence models remain authoritative in `libs/schemas`; cross-service synchronous and asynchronous payloads are published through `libs/contracts`; shared policy vocabulary is published through `libs/policy`; all cross-boundary surfaces use semantic versioning and coordinated compatibility review.
- Consequences:
  - generated client types are derived artifacts rather than authoritative sources
  - breaking payload or enum changes require explicit compatibility review and a major-version step
  - event payloads must carry `schema_version` and may not silently repurpose prior meanings

## D-013: Repository Python Bootstrap Is uv-Locked At The Root Until The First Multi-Package Split

- Date: 2026-03-06
- Status: accepted
- Context: the architecture selected `uv`, and the repository now has a normalized `uv` bootstrap, but the codebase still contains only one real Python package under `libs/schemas`.
- Decision: the root `pyproject.toml` and `uv.lock` remain the authoritative Python bootstrap surface until the first additional Python package is added, at which point the package-manifest split must happen deliberately as a bounded Phase 01 change instead of informally.
- Consequences:
  - `uv sync --dev` is the required Python bootstrap command
  - new Python service or library packages may not be added ad hoc under the old single-package assumption
  - Phase 01 must treat the package-boundary transition as explicit work, not accidental drift

## D-014: Shared Library Source Roots Expand Under The Root Toolchain Before Service-Level Packaging

- Date: 2026-03-06
- Status: accepted
- Context: `P01-T01` is now executing the first deliberate Phase 01 package-boundary transition. The repository needs executable `libs/contracts` and `libs/policy` packages immediately, but it does not yet need fully separate service-level Python project manifests.
- Decision: the root `uv` bootstrap remains authoritative while the repository adds `libs/contracts/src` and `libs/policy/src` as first-party shared-library source roots. Repository-local tests and static analysis must include every shared-library source root explicitly until a later bounded service-level packaging split occurs.
- Consequences:
  - root Python validation commands must include `libs/schemas/src`, `libs/contracts/src`, `libs/policy/src`, and `tests`
  - new shared-library handwritten code must reach 100 percent coverage before `P01-T01` can close
  - later service runtime packaging work must still make an explicit decision about per-service manifests rather than assuming this interim source-root model is final

## D-015: Phase 01 Infrastructure Begins With Provider-Neutral Blueprints

- Date: 2026-03-06
- Status: accepted
- Context: `P01-T02` needs to move the repository forward before the final deployment environment and budget envelope are chosen, but the architecture and PM baseline explicitly forbid unsafe provider assumptions.
- Decision: the first `P01-T02` slice will publish provider-neutral Terraform module contracts, provider-neutral environment blueprints, logical node-pool aliases, logical storage-profile aliases, and a Helm platform-foundation chart without introducing provider-specific resources, IAM bindings, DNS integrations, or concrete storage classes.
- Consequences:
  - `infra/terraform` and `infra/helm` become durable control-plane baselines even before provider-specific provisioning begins
  - provider-specific `P01-T02-S02` work remains blocked on `OQ-01` and `OQ-02`
  - repository tests must lock provider neutrality so blueprint-only infrastructure is not mistaken for deploy-ready infrastructure

## D-016: Local Development Standardizes On A kind-Based Self-Managed Cluster Target

- Date: 2026-03-06
- Status: accepted
- Context: the repository needed an executable self-managed Kubernetes target to continue Phase 01 locally, but the higher-environment hosting decision tracked in `OQ-01` remains unresolved and the architecture forbids silently choosing a provider.
- Decision: local development will standardize on an internal-only `kind` cluster running on Docker, with one control-plane node, three labeled worker nodes that simulate the `general`, `stateful`, and `gpu` workload roles, and local Helm validation against that cluster. This decision narrows `OQ-01` and the safe local portion of `OQ-02` for `Local` development only. It does not choose a shared dev, staging, pilot, or production environment.
- Consequences:
  - Phase 01 can validate cluster bootstrap, namespace conventions, priority classes, and local control-plane behavior without waiting for a higher-environment provider decision
  - local storage aliases may collapse to simple development defaults as long as they remain explicitly non-production-authoritative
  - local `kind` validation may not be cited as evidence for higher-environment readiness, sizing, backup, DNS, IAM, or GPU guarantees
  - provider-specific `P01-T02` follow-on work remains blocked until `OQ-01` and `OQ-02` are narrowed for higher environments

## D-017: Local GitOps Uses The Public Repository URL But Distinguishes Direct Bootstrap From Live Reconciliation

- Date: 2026-03-06
- Status: accepted
- Context: `P01-T03` now needs a real Local GitOps baseline on top of the validated `kind` target, and the repository already has a public Git remote on `main`. At the same time, local validation must be able to exercise current manifests before those exact changes are necessarily present on the tracked remote branch.
- Decision: the Local Argo CD baseline will point at `https://github.com/bcdannyboy/MapTheIsland.git` on branch `main`, publish repo-managed bootstrap and child `Application` manifests, and treat that Git remote as the authoritative desired-state source. Direct local Helm and `kubectl` bootstrap commands remain allowed for Local validation only and may not be treated as proof that live Git reconciliation has already been exercised for the same repo state.
- Consequences:
  - the repo has a concrete Local GitOps target rather than a file-path-only shortcut
  - Local validation can keep moving without requiring a push for every intermediate manifest edit
  - future Phase 01 closeout must explicitly validate or re-baseline the live tracked-remote reconciliation step before claiming full `P01-T03` closure

## D-018: Local Secret Bootstrap Uses Gitignored Vault Dev Tokens And Namespace-Scoped Delivery

- Date: 2026-03-06
- Status: accepted
- Context: `GAP-012` blocked `P01-T03-S02` because the architecture specified Vault plus External Secrets but left the Local trust chain and namespace segmentation undefined.
- Decision: Local secret bootstrap will generate gitignored Vault dev-token material under `.state/kind/`, mirror only the required bootstrap token into `maptheisland-dev-foundation-system`, define a `ClusterSecretStore` that reads that token, and materialize runtime secrets only into the consuming namespace through `ExternalSecret`. Literal secret values may not be committed to Git.
- Consequences:
  - Local secret delivery now has an explicit trust chain and tenancy model
  - sample workloads can validate namespace-local runtime secret delivery without cross-namespace secret sharing
  - higher-environment auth backend and tenancy details remain separately unresolved and may not silently inherit the Local bootstrap shortcut

## D-019: Local Tracked-Remote GitOps Validation Declares Stable ExternalSecret Defaults And Forces A Root Refresh

- Date: 2026-03-06
- Status: accepted
- Context: the remaining Local `P01-T03` closeout work surfaced two operational failure modes that were not architectural blockers but did make the tracked-remote GitOps gate noisy and brittle: External Secrets defaults caused false `OutOfSync` drift in Argo CD, and Argo CD could legitimately keep an older Git revision cached until the next poll even after the tracked remote had been updated.
- Decision: the Local sample `ExternalSecret` manifest must declare the stable controller-defaulted fields that materially affect Argo CD sync, and the published tracked-remote validation command must hard-refresh the Local bootstrap `Application` before waiting for the target Git revision and child-application convergence.
- Consequences:
  - the Local tracked-remote validation command now measures real manifest drift instead of defaulted-spec churn
  - the Local GitOps proof path is more deterministic and no longer depends on controller poll timing alone
  - future Local control-plane manifests that show the same default-mutation pattern must either declare those defaults explicitly or justify a narrower ignore-differences rule

## Pending Decisions

Use `proposed` entries here for future architectural or delivery changes. Do not edit accepted entries except to add a superseding record.
