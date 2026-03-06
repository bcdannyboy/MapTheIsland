# Engineering Standards Baseline

## Purpose

This document is the detailed `P00-T05` engineering baseline for repository
structure, local bootstrap, lockfiles, validation commands, CI expectations,
and contribution rules.

The architecture is explicit that this repository is a platform monorepo, not a
single application. These standards therefore prioritize deterministic
bootstrap, strong local validation, and clear cross-language ownership.

## Repository Structure Standard

| Path | Standard | Notes |
| --- | --- | --- |
| `infra/` | infrastructure code only | provider, network, cluster, stateful-service, and deployment definitions |
| `services/` | first-party service runtimes | one service per directory, `src/` layout once code exists |
| `apps/` | analyst-facing application packages | `apps/web` is the first application package |
| `libs/` | shared cross-service libraries | shared schemas, contracts, policy, prompts, and evaluation helpers |
| `docs/implementation/` | human-readable implementation baseline | authoritative Phase 00 and follow-on implementation docs |
| `tests/` | repository-level Python tests and future cross-package integration suites | retained at root until multi-package Python service work requires package-local split |

## Python Workspace Standard

- `uv` is the canonical Python bootstrap and lockfile manager.
- `uv.lock` is a required repository artifact.
- The root `pyproject.toml` currently owns shared tool configuration and the
  current shared-library Python source roots.
- Phase 01 has now executed the deliberate shared-library package-boundary
  transition for:
  - `libs/schemas/src/maptheisland_schemas`
  - `libs/contracts/src/maptheisland_contracts`
  - `libs/policy/src/maptheisland_policy`
- Additional Python packages may not be added informally; each new shared
  library or service package still requires an explicit bounded change.
- New Python libraries and services must use `src/` layout when they are added.
- All non-trivial modules, public functions, public classes, validators, and
  helpers require docstrings.
- Python bootstrap commands are:
  - `uv sync --dev`
  - `uv run ruff check .`
  - `uv run mypy libs/schemas/src libs/contracts/src libs/policy/src tests`
  - `uv run pytest`

## Frontend Workspace Standard

- `pnpm` is the canonical JavaScript and TypeScript workspace manager.
- The root workspace remains scoped to `apps/*` and `libs/*` until a real JS or
  TS shared library exists.
- `pnpm-lock.yaml` is a required repository artifact once web dependencies are
  installed.
- `apps/web` remains the only application package until later analyst-facing
  applications exist.
- Frontend bootstrap and validation commands are:
  - `pnpm install`
  - `pnpm typecheck:web`
  - `pnpm test:web:unit`
  - `pnpm test:web:e2e`
- End-to-end Playwright checks become gating once browser routes and fixtures
  exist; until then, the e2e command may pass with no tests while typecheck and
  unit coverage remain the enforced baseline.

## Local Validation Standard

The repository-level local validation baseline is:

- Python lint: `uv run ruff check .`
- Python typing: `uv run mypy libs/schemas/src libs/contracts/src libs/policy/src tests`
- Python tests and coverage: `uv run pytest`
- Web type validation: `pnpm typecheck:web`
- Web config and support-code unit coverage: `pnpm test:web:unit`
- Web end-to-end validation: `pnpm test:web:e2e` once runtime routes exist
- Infrastructure validation: `pnpm check:infra`
- Internal-only local cluster bootstrap:
  - `pnpm create:kind:dev`
  - `pnpm check:kind:nodes`
  - `pnpm check:kind:foundation`
  - `pnpm delete:kind:dev`
- Repository tests also lock critical declarative infrastructure and workflow
  surfaces when those artifacts are handwritten and executable behavior depends
  on them

No handwritten code change is complete unless relevant tests pass at 100 percent
and handwritten-code coverage remains at 100 percent for the affected scope.

## Infrastructure Baseline Standard

- Provider-neutral Terraform and Helm baselines may land before a concrete
  hosting target is chosen, but they must remain explicit about unresolved
  provider-specific behavior.
- Logical storage profiles, node-pool roles, environment naming, and namespace
  conventions are allowed in advance of a provider decision.
- Provider-specific resource types, IAM backends, storage classes, DNS zones,
  and ingress controllers may not be committed under the guise of neutral
  scaffolding.
- Repository tests should cover critical declarative expectations until direct
  Terraform or Helm validation becomes a stable local requirement.
- The current local-dev infrastructure target also requires `kind` for cluster
  bootstrap and `helm` for chart lint and render validation.
- The root infrastructure command surface is:
  - `pnpm lint:tf`
  - `pnpm validate:tf:dev`
  - `pnpm lint:helm`
  - `pnpm template:helm:kind-dev`
  - `pnpm check:infra`

## CI And Review Baseline

CI must remain path-aware but enforce one consistent quality policy:

- Python changes run `uv sync --dev`, Ruff, mypy, and pytest.
- Web changes run `pnpm install --frozen-lockfile`, `pnpm typecheck:web`, and
  the applicable Playwright suite once route code exists.
- Schema, contract, or policy changes run both Python and web checks whenever a
  downstream consumer exists.
- The initial repository workflow is `.github/workflows/ci.yml`, which runs the
  published Python, infrastructure, and web quality gates and installs the
  required language or infra tooling explicitly per job.
- Review may not approve a change that lowers handwritten-code coverage below
  100 percent or leaves any local or integration test failing.
- Contract changes require architecture review plus review from at least one
  affected consumer owner.
- Policy-sensitive changes require policy and security review.
- BFF/browser boundary changes require BFF/API and frontend review together.

## Contribution Rules

- Update PM docs and implementation docs in the same session as any material
  behavior, contract, tooling, or risk change.
- Add tests in the same change set as new handwritten code.
- Prefer the shared library surfaces over local copy-and-paste types or enums.
- Keep service-specific runtime concerns out of `apps/web`.
- Keep browser logic out of direct datastore and model-provider access paths.
- Record durable design choices in `pm/07_decision_log.md`.

## Current Transition Note

Phase 00 normalized the Python bootstrap with `uv`, and Phase 01 has now used
that root-controlled bootstrap to add executable shared-library source roots for
`contracts` and `policy`. This preserves one authoritative toolchain surface
while making the shared-library boundary explicit. Future service packages still
require a deliberate follow-on boundary change rather than ad hoc growth.

## References

- `Architecture_Plan.md`, section 2 and Part II section 17
- `pyproject.toml`
- `package.json`
- `pnpm-workspace.yaml`
- `apps/web/README.md`
