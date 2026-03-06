# Environment And Promotion Model

This document defines how code, schemas, infrastructure, and data move through environments. It exists so environment decisions are not improvised later.

## Environment Set

### Local

- purpose: individual development, fast iteration, contract validation, and targeted testing
- allowed data: synthetic samples, minimal public sample subsets, or explicitly approved local fixtures
- promotion rule: nothing promotes directly from local to pilot or production
- local control-plane note: Local may use direct bootstrap commands for Argo CD, Vault, External Secrets, cert-manager, and sample validation resources before the same repo state is proven through tracked-remote Git reconciliation; that direct bootstrap is a validation aid only and not promotion evidence

### Dev

- purpose: shared integration environment for service compatibility and workflow validation
- allowed data: controlled sample subsets and non-sensitive test fixtures
- promotion rule: code and schema changes must pass CI before entry

### Staging

- purpose: pre-release environment for realistic end-to-end validation and release rehearsal
- allowed data: curated representative datasets approved for staging use
- promotion rule: only release-candidate code and approved schema migrations

### Pilot

- purpose: restricted analyst-facing environment for controlled real-world usage
- allowed data: approved pilot corpus slices and role-restricted access paths
- promotion rule: requires milestone package and signoff

### Production

- purpose: approved operational environment
- allowed data: approved live corpus and approved role-based workflows
- promotion rule: requires production readiness evidence and rollback path

## Promotion Objects

The following move independently and must be tracked explicitly:

- application code
- infrastructure definitions
- database schema and migrations
- search mappings and index versions
- graph projections
- analytical asset definitions
- model prompts and evaluation thresholds
- data branches or snapshots
- secrets and credential material

## Promotion Rules

- code promotion requires passing environment-specific validation
- schema promotion requires forward and rollback procedure documentation
- data promotion requires explicit source lineage and validation evidence
- prompt or threshold promotion requires evaluation evidence
- secret rotation follows environment-specific secure-delivery procedures and is never bundled as plaintext in repo changes
- Local bootstrap tokens or sample secret seed material may exist only in gitignored local state or namespace-local bootstrap secrets and are never promotable artifacts

## Migration Discipline

- database migrations must be versioned
- search or graph schema changes must record reindex or rematerialization expectations
- Iceberg or analytical asset changes must record snapshot implications
- environment promotion may be blocked if rollback is undefined

## Rollback Discipline

Every promoted release must identify:

- previous known-good code state
- migration rollback or remediation path
- data rematerialization or reindex procedure
- feature-flag or endpoint-disable path where applicable

## Temporary Exception Rule

Any emergency deviation from the environment or promotion model must be:

- logged in the session log
- added to the decision log if durable
- followed by a cleanup or automation task
