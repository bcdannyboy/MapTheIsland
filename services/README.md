# Service Workspace

This directory fixes the initial service boundary surface from the architecture.
Current service directories are placeholders only; they exist so later work does
not collapse responsibilities or invent new top-level layout.

## Phase 01 Contribution Rule

Phase 01 does not turn every reserved service into runtime code immediately.
Instead, it keeps the service workspace structurally stable so later phases can
add service packages without top-level churn.

## Reserved Services

- `harvester`
- `docproc`
- `ocr`
- `extractor`
- `resolver`
- `topics`
- `graph-builder`
- `indexer`
- `review-api`
- `qa-orchestrator`
- `bff`

## Expected Per-Service Layout Once A Service Activates

When a reserved service becomes active, its directory should grow into a
bounded package rather than a loose collection of files:

```text
services/<service-name>/
  README.md
  src/<service_module>/
    __init__.py
  tests/
```

Additional runtime-specific files may be added later, but the service must keep
its source root, tests, and ownership documentation explicit.

## Operational Endpoint Baseline

Every long-lived service runtime is expected to expose these operational
endpoints once implementation begins:

- `GET /health/live`
- `GET /health/ready`
- `GET /metrics`
- `GET /version`
- `GET /openapi.json`

These are operational surfaces, not browser-facing business APIs. Browser
traffic still belongs behind `bff`.

## Ownership And Contribution Path

- Use `docs/implementation/service-boundaries-and-contracts.md` as the
  authoritative source for reserved service responsibility and first-delivery
  phase.
- Publish cross-boundary payloads through `libs/contracts`, not inside a
  service-local module.
- Publish shared policy semantics through `libs/policy`, not inside a
  service-local module.
- Add service-specific implementation packages only when the relevant phase task
  is active and the package boundary has a clear owner.
