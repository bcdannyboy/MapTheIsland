# `@maptheisland/web`

Phase 00 frontend workspace baseline for the MapTheIsland evidence workbench.

This directory intentionally contains documentation and configuration only. It does not yet contain runtime application code, route implementations, authentication wiring, or UI components. The purpose of this baseline is to lock the workspace shape, package metadata, TypeScript defaults, and Playwright expectations before Phase 06 implementation work begins.

## Scope Of This Baseline

- Establish the `apps/web` package as the future Next.js App Router application.
- Encode the frontend toolchain baseline around `pnpm`, TypeScript, and Playwright.
- Freeze the route inventory and BFF contract expectations implied by `Architecture_Plan.md`.
- Avoid adding any application runtime code before the BFF contracts and policy envelopes are implemented.

## Explicit Non-Goals

- No `app/` directory yet.
- No page, layout, component, hook, or state-management code yet.
- No direct browser integrations with PostgreSQL, OpenSearch, Neo4j, Trino, or model providers.
- No mock data layer that would let later work drift away from the architecture.

## Route Expectations

The eventual route structure must follow the architecture and PM baseline:

- `/search`
- `/documents/[documentId]`
- `/entities/[entityId]`
- `/events/[eventId]`
- `/topics/[topicId]`
- `/graph`
- `/timeline`
- `/review`
- `/qa`
- `/admin`

Route implementation requirements:

- The web app is an evidence workbench, not a generic chatbot shell.
- Route state must be deterministic and URL-addressable so analyst views can be bookmarked, cited, and reproduced.
- Search is the default analyst entry point.
- Document viewing is the evidentiary center of the product and must later support image, native-text, and OCR-layer switching.
- Graph rendering must remain bounded to server-materialized subgraphs; the browser must never request or hold the entire corpus graph.
- Restricted surfaces such as redaction analysis and review tooling must remain policy-mediated.

## Contract Expectations

The browser must treat the FastAPI backend-for-frontend as its only privileged data surface. Future runtime code in this package must assume:

- all privileged reads are BFF-mediated
- the browser never talks directly to datastore backends
- the browser never talks directly to model providers
- auth and role resolution are enforced before data is exposed to route code

Every relevant BFF response is expected to expose:

- `policy_context`
- `provenance_summary`
- `result_confidence`

Frontend code added later must not infer those fields client-side. If a route cannot show its policy scope, provenance basis, or confidence status from server data, the route is incomplete.

## Planned Frontend Stack

This baseline pins only the minimum package set needed to establish the application shell and testing foundation:

- `next`
- `react`
- `react-dom`
- `typescript`
- `@playwright/test`

Architecture-named libraries such as TanStack Query, PDF.js, Cytoscape.js, Apache ECharts, `zod`, and `react-hook-form` are intentionally not pinned yet in this Phase 00 scaffold. They should be added when the corresponding implementation work begins so their versions are chosen in context of actual route and contract code.

## TypeScript Expectations

The TypeScript baseline is intentionally strict:

- `strict` mode is on.
- `noEmit` is on because build artifacts should be produced by Next.js, not raw `tsc`.
- `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` are enabled to reduce silent contract drift.
- `moduleResolution` is set for modern bundler behavior consistent with a Next.js application package.

When runtime code is added later:

- shared contracts should come from workspace libraries rather than ad hoc local type duplication
- route params, search params, and BFF payloads should be parsed explicitly
- policy-sensitive fields should remain typed all the way to the UI boundary

## Playwright Expectations

Playwright is included as the browser-level validation baseline because the architecture requires route smoke coverage and end-to-end workflow validation for evidence navigation, review flows, and policy-safe rendering.

The current config establishes:

- `tests/e2e` as the default test directory inside `apps/web`
- HTML and console reporters
- failure-only screenshots and videos
- trace collection on first retry
- Chromium, Firefox, and WebKit project baselines

What is intentionally deferred:

- automatic `webServer` startup
- seeded test data
- auth fixtures
- route-specific smoke tests
- CI-specific sharding

Those additions should happen only once the Next.js shell and BFF contract surfaces exist.

## Root Workspace Commands

The repository-level workspace expects:

- `pnpm install` to materialize `pnpm-lock.yaml`
- `pnpm typecheck:web` for the baseline frontend validation surface
- `pnpm test:web:unit` to keep executable support code under coverage
- `pnpm test:web:e2e` once route code and fixtures exist

Cross-language Python validation remains rooted at the repo root through `uv`
and is documented in `docs/implementation/engineering-standards-baseline.md`.

## Testing Expectations For Future Implementation

When runtime code arrives, frontend verification is expected to layer as follows:

1. Type-level validation via `tsc`.
2. Unit coverage for executable configuration and other non-route support code.
3. Route-level smoke checks for primary analyst surfaces.
4. Browser-level end-to-end flows in Playwright.

Minimum future Playwright coverage should include:

- route reachability for `/search`, `/documents/[documentId]`, `/entities/[entityId]`, `/events/[eventId]`, `/review`, and `/qa`
- deep-link navigation from cited answers into supporting document spans
- policy-safe rendering for restricted content
- failure handling for missing support, denied access, and long-running job polling

## Ownership Boundary

This package owns only browser-side application concerns. It must not absorb:

- backend orchestration logic
- datastore clients
- policy decision authority
- evidence provenance computation

Those remain upstream concerns of the BFF and backend services. The web app renders and inspects those outcomes; it does not originate them.
