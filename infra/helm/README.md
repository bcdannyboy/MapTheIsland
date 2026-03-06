# Helm Baseline

This directory contains the provider-neutral `P01-T02` Helm baseline plus the
Local-only `P01-T03` values surfaces for upstream control-plane charts.

## Current Scope

The first chart under this directory establishes:

- namespace conventions for control-plane, data-plane, and application
  workloads
- cluster-wide workload-priority intent aligned to the architecture's node-pool
  model
- values-schema validation for the provider-neutral foundation chart
- local-dev values for the internal-only `kind` target
- pinned Local values for Argo CD, Vault, External Secrets Operator, and
  cert-manager under `infra/helm/values/control-plane/`

## Explicit Deferrals

This directory still does not yet own:

- stateful service dependencies
- first-party runtime services
- higher-environment control-plane values

The Local control-plane values published here are development baselines only.
They do not select a higher-environment provider, CA model, or secret auth
backend.

For local validation, use `values.kind-dev.yaml` with the foundation chart. It
maps the provider-neutral storage aliases and namespace prefix into an
internal-only development target without implying that a higher-environment
storage-class or provider decision has been made.
