# Open Questions

These are unresolved inputs that should not be silently assumed.

## OQ-01: Deployment Environment

- Question: which higher-environment self-managed target will host the shared dev, staging, pilot, and production Kubernetes surfaces after the local development target?
- Why it matters: affects provider-specific Terraform resources, storage classes, IAM model, backups, DNS, and networking outside the now-defined local development target.
- Decision owner: platform or infrastructure lead with architecture lead review
- Decision deadline: before provider-specific `P01-T02-S02` implementation begins
- Acceptable provisional fallback: the internal-only local `kind` target recorded in `D-016`, plus environment-agnostic Terraform module design for higher environments
- Work that can continue safely while unresolved:
  - local-dev `P01-T02` bootstrap and validation
  - internal-only `P01-T03`
  - local-only `P01-T04` scaffolding that does not imply higher-environment provider choices
  - repo scaffolding and shared contract work
- Blocks:
  - provider-specific `P01-T02-S02`
  - higher-environment `P01-T03`
  - higher-environment `P01-T04`

## OQ-02: Budget And Capacity Envelope

- Question: what budget and throughput assumptions apply for GPU, storage, and stateful workloads?
- Why it matters: affects node pool sizing, retention, OCR throughput, and rollout timing.
- Decision owner: program manager with platform and data-plane input
- Decision deadline: before capacity-sensitive `P01-T02-S02`, before `P01-T04`, and before production-scale `P02-T03`
- Acceptable provisional fallback: the small-footprint local `kind` posture recorded in `docs/implementation/local-dev-platform-target.md`, with no higher-environment or production-authoritative claims
- Work that can continue safely while unresolved:
  - internal-only `P01-T02`
  - internal-only `P01-T03`
  - local-only `P01-T04` scaffolding
  - evaluation harness design
  - small-sample pipeline development
- Blocks:
  - capacity-sensitive `P01-T02-S02`
  - higher-environment `P01-T04`
  - production-scale `P02-T03`

## OQ-03: Restricted Role Governance

- Question: who approves role definitions, restricted views, and export rules?
- Why it matters: the policy model cannot be finalized without an authority path.
- Decision owner: policy and security lead with program manager coordination
- Decision deadline: before `P03-T02` promotion and before any restricted-feature preview
- Acceptable provisional fallback: internal-only deny-by-default restricted-role model
- Work that can continue safely while unresolved:
  - evidence processing
  - review infrastructure scaffolding
  - public-role UI and BFF work
- Blocks:
  - P03-T02
  - P03-T03
  - P07-T04

## OQ-04: Release Audience And Pilot Cohort

- Question: who is the intended audience for internal alpha, analyst preview, and restricted pilot?
- Why it matters: affects BFF authorization, UI expectations, observability scope, and release criteria.
- Decision owner: program manager with release lead and application lead input
- Decision deadline: before `P06-T07`
- Acceptable provisional fallback: internal engineering and internal reviewer audience only
- Work that can continue safely while unresolved:
  - backend and UI implementation
  - internal-only validation
  - evidence workbench MVP hardening short of preview approval
- Blocks:
  - P06-T07
  - P07-T04

## OQ-05: Gold-Set Curation Ownership

- Question: who curates and signs off evaluation datasets for OCR, extraction, retrieval, and QA?
- Why it matters: quality gates depend on evaluated thresholds, not ad hoc confidence.
- Decision owner: release lead with semantics and document-processing input
- Decision deadline: before `P05-T06`
- Acceptable provisional fallback: internal provisional gold sets marked non-release-authoritative
- Work that can continue safely while unresolved:
  - pipeline development
  - instrumentation
  - non-promotional experimentation
- Blocks:
  - P05-T06
  - P07-T04
