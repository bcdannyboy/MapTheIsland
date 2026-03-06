# PM Workspace Change Log

## 2026-03-06

- Created the initial persistent `/pm` workspace.
- Added charter, constraints, delivery model, phase plan, dependency map, workstream index, risk register, decision log, research register, quality gates, release strategy, and status dashboard.
- Established the first release boundary as the policy-safe evidence workbench.
- Initialized planning status at Phase 00.
- Added a second-pass documentation expansion with glossary, artifact inventory, non-functional requirements, decision boundaries, and phase interlocks.
- Expanded phase files with handoff summaries, artifact boundaries, blocking open-question visibility, and signoff roles.
- Strengthened PM controls to make 100 percent coverage and 100 percent local and integration test pass rates explicit hard gates.
- Added the executable Phase 00 implementation baseline under `docs/implementation/`.
- Added the initial shared schema package under `libs/schemas/` with complete local test, lint, and type-check coverage.
- Added the monorepo directory scaffold, root Python tooling config, and frontend workspace baseline.
- Added bounded Phase 00 work packages for `P00-T03`, `P00-T04`, and `P00-T05`.
- Published detailed Phase 00 implementation baselines for policy, service boundaries, contracts, and engineering standards.
- Normalized the Python bootstrap with `uv`, committed `uv.lock`, and added root Python validation scripts.
- Added centralized contract and policy artifact definitions plus durable contract-governance decisions.
- Completed `P01-T01` with executable `libs/contracts` and `libs/policy` packages, shared-library ownership guidance, and expanded Python validation across all shared-library source roots.
- Added the initial repository CI workflow plus root `check:web` automation and a regression test for the CI baseline, partially completing `P01-T06`.
- Re-baselined the Phase 01 dashboard, backlog, session log, and work packages around completed `P01-T01`, partially completed `P01-T06`, and the next ready provider-neutral `P01-T02` lane.
- Added the first provider-neutral `P01-T02` infrastructure baseline under `infra/terraform/` and `infra/helm/`, plus Phase 01 implementation documentation, decision logging, and repository tests for the new declarative surfaces.
- Narrowed `OQ-01` and the safe local portion of `OQ-02` into an internal-only `kind`-based local development target, added local infra validation commands, and extended the implementation docs and repository tests around that executable baseline.
- Added the first internal-only `P01-T03` control-plane baseline under `infra/gitops/` and `infra/helm/values/control-plane/`, published the Local GitOps and secret-bootstrapping rules, and validated the Local secret plus certificate delivery path on `kind`.
