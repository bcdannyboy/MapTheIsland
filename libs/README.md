# Shared Library Workspace

This directory holds cross-service libraries whose contracts must remain stable
across the repository.

## Phase 01 Status

Phase 01 has started the deliberate shared-library package-boundary transition.
The workspace now contains:

- `schemas/`: canonical evidence and shared validation models
- `contracts/`: executable async event and service-boundary contract baseline
- `policy/`: executable shared policy vocabulary, deny-by-default matrices, and
  prohibited-flow constants
- `prompts/`: reserved for later model-assisted prompt assets
- `evaluation/`: reserved for later evaluation fixtures and regression helpers

## Source Roots

The current Python source roots are:

- `libs/schemas/src/maptheisland_schemas`
- `libs/contracts/src/maptheisland_contracts`
- `libs/policy/src/maptheisland_policy`

The root `pyproject.toml` remains the authoritative Python bootstrap surface,
and repository-level tests and typing checks load all three source roots
together.

## Ownership And Contribution Path

| Library | Primary owner role | When to edit it | Required co-review |
| --- | --- | --- | --- |
| `schemas/` | architecture lead | canonical evidence, provenance, review-state, or sensitivity schema changes | data and orchestration lead; BFF/API lead for cross-boundary changes |
| `contracts/` | BFF and API lead | async event, operational, or cross-service payload changes | architecture lead plus at least one consuming owner |
| `policy/` | policy and security lead | shared role, export, or deny-by-default vocabulary changes | architecture lead and affected consuming owner |
| `prompts/` | semantics or QA lead | prompt assets and routing metadata once prompt work begins | policy and security lead |
| `evaluation/` | evaluation and release lead | evaluation fixtures, metrics helpers, and thresholds once evaluation work begins | affected workflow owner |

If a change affects cross-boundary semantics, update the relevant implementation
docs and PM artifacts in the same session rather than relying on code alone.
