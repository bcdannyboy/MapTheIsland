"""Repository tests for the internal-only local kind development target."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KIND_ROOT = REPO_ROOT / "infra" / "kind"
HELM_ROOT = REPO_ROOT / "infra" / "helm" / "charts" / "platform-foundation"


def test_kind_local_dev_target_files_exist() -> None:
    """The local-dev kind baseline should publish its config and readme."""
    expected_paths = (
        KIND_ROOT / "README.md",
        KIND_ROOT / "dev-cluster.yaml",
        HELM_ROOT / "values.kind-dev.yaml",
    )

    missing_paths = [path for path in expected_paths if not path.exists()]
    assert missing_paths == []


def test_kind_local_dev_target_remains_internal_only() -> None:
    """The local-dev target docs should stay explicit about their limited scope."""
    readme = (KIND_ROOT / "README.md").read_text(encoding="utf-8")

    assert "internal-only" in readme
    assert "staging, pilot, or production" in readme
    assert "does not claim" in readme


def test_kind_cluster_config_models_control_plane_and_logical_worker_roles() -> None:
    """The kind cluster config should simulate the architecture's node-pool roles."""
    cluster_config = (KIND_ROOT / "dev-cluster.yaml").read_text(encoding="utf-8")

    assert "kind.x-k8s.io/v1alpha4" in cluster_config
    assert cluster_config.count("role: worker") == 3
    assert "maptheisland.io/nodepool=general" in cluster_config
    assert "maptheisland.io/nodepool=stateful" in cluster_config
    assert "maptheisland.io/nodepool=gpu" in cluster_config
    assert "maptheisland.io/accelerator=true:NoSchedule" in cluster_config


def test_kind_values_align_with_platform_foundation_contracts() -> None:
    """The local-dev Helm values should preserve the foundation chart contract."""
    kind_values = (HELM_ROOT / "values.kind-dev.yaml").read_text(encoding="utf-8")

    assert "namespacePrefix: maptheisland-dev" in kind_values
    assert "foundation-system" in kind_values
    assert "foundation-observability" in kind_values
    assert "general:" in kind_values
    assert "stateful_ssd: standard" in kind_values
    assert "gpu_scratch: ephemeral" in kind_values
