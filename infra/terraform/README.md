# Terraform Baseline

This directory contains the provider-neutral Terraform baseline for `P01-T02`.

## Layout

```text
infra/terraform/
  versions.tf
  environments/
    dev/
  modules/
    networking/
    storage/
    dns/
    identity/
    cluster/
```

## Current Intent

The current baseline fixes:

- module boundaries for networking, storage, DNS, identity, and cluster intent
- a provider-neutral `dev` environment blueprint
- logical node-pool roles for `general`, `stateful`, and `gpu`
- logical storage-profile aliases that later provider-specific work must map to

## Explicit Non-Goals Of This Slice

The current Terraform baseline does not yet:

- create cloud, on-prem, or hosted provider resources
- choose one IAM, DNS, or object-storage implementation
- define storage classes for a specific cluster
- claim that a live environment can already be applied

Those decisions remain blocked until the deployment environment is selected. The
current baseline exists so later provider-specific work inherits stable module
contracts instead of inventing them ad hoc.
