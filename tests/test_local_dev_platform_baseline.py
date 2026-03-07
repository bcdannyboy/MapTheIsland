"""Regression checks for the internal-only local development cluster baseline."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KIND_ROOT = REPO_ROOT / "infra" / "kind"
HELM_ROOT = REPO_ROOT / "infra" / "helm" / "charts" / "platform-foundation"


def test_kind_local_dev_target_exists_with_expected_node_pool_markers() -> None:
    """The local dev target should simulate the architecture's workload classes."""
    cluster_config = (KIND_ROOT / "dev-cluster.yaml").read_text(encoding="utf-8")

    assert "kind: Cluster" in cluster_config
    assert "kind.x-k8s.io/v1alpha4" in cluster_config
    assert cluster_config.count("- role: worker") == 3
    assert "maptheisland.io/nodepool=general" in cluster_config
    assert "maptheisland.io/nodepool=stateful" in cluster_config
    assert "maptheisland.io/nodepool=gpu" in cluster_config
    assert "register-with-taints" in cluster_config


def test_kind_local_dev_docs_preserve_internal_only_scope() -> None:
    """The local dev target must not be mistaken for a higher-environment choice."""
    readme = (KIND_ROOT / "README.md").read_text(encoding="utf-8")

    assert "internal-only" in readme
    assert "does not claim" in readme
    assert "staging, pilot, or production" in readme
    assert "pnpm create:kind:dev" in readme
    assert "pnpm check:control-plane" in readme
    assert "pnpm delete:kind:dev" in readme


def test_kind_dev_values_file_aligns_with_chart_contract() -> None:
    """The kind values file should satisfy the chart's required keys."""
    required_keys = json.loads((HELM_ROOT / "values.schema.json").read_text(encoding="utf-8"))[
        "required"
    ]
    values_text = (HELM_ROOT / "values.kind-dev.yaml").read_text(encoding="utf-8")

    for required_key in required_keys:
        assert f"{required_key}:" in values_text

    assert "namespacePrefix: maptheisland-dev" in values_text
    assert "gpu_scratch: ephemeral" in values_text


def test_root_workspace_exposes_infra_and_local_dev_commands() -> None:
    """The repo root should publish the infra and local-dev command surface."""
    package_manifest = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package_manifest["scripts"]

    assert package_manifest["version"] == "0.1.0-phase-01"
    assert "Phase 01 platform foundation baseline" in package_manifest["description"]
    assert scripts["lint:tf"] == "terraform fmt -check -recursive infra/terraform"
    assert "TF_DATA_DIR=$PWD/.terraform-cache/dev" in scripts["validate:tf:dev"]
    assert "terraform -chdir=infra/terraform/environments/dev init -backend=false" in scripts[
        "validate:tf:dev"
    ]
    assert "values.kind-dev.yaml" in scripts["lint:helm"]
    assert "values.kind-dev.yaml" in scripts["template:helm:kind-dev"]
    assert scripts["check:infra"] == (
        "pnpm lint:tf && pnpm validate:tf:dev && pnpm lint:helm && pnpm template:helm:kind-dev"
    )
    assert "kind create cluster --name maptheisland-dev" in scripts["create:kind:dev"]
    assert "--config infra/kind/dev-cluster.yaml" in scripts["create:kind:dev"]
    assert "--kubeconfig .state/kind/kubeconfig" in scripts["create:kind:dev"]
    assert "kind delete cluster --name maptheisland-dev" in scripts["delete:kind:dev"]
    assert "rm -f .state/kind/kubeconfig" in scripts["delete:kind:dev"]
    assert "helm upgrade --install maptheisland-platform" in scripts["apply:kind:foundation"]
    assert "values.kind-dev.yaml" in scripts["check:kind:foundation"]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["apply:kind:foundation"]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["check:kind:foundation"]


def test_gitignore_covers_phase_01_generated_validation_artifacts() -> None:
    """Generated infra and coverage artifacts should stay out of source control."""
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

    for pattern in (
        ".terraform/",
        ".terraform-cache/",
        "coverage/",
        "**/coverage/",
        "*.egg-info/",
        "*.tsbuildinfo",
    ):
        assert pattern in gitignore
