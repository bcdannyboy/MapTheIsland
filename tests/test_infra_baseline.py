"""Repository tests for the provider-neutral Phase 01 infrastructure baseline."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TERRAFORM_ROOT = REPO_ROOT / "infra" / "terraform"
HELM_ROOT = REPO_ROOT / "infra" / "helm" / "charts" / "platform-foundation"
KIND_ROOT = REPO_ROOT / "infra" / "kind"


def test_terraform_module_map_and_environment_blueprint_exist() -> None:
    """The provider-neutral Terraform baseline should expose the expected modules."""
    expected_paths = (
        TERRAFORM_ROOT / "versions.tf",
        TERRAFORM_ROOT / "environments" / "dev" / "main.tf",
        TERRAFORM_ROOT / "environments" / "dev" / "outputs.tf",
        TERRAFORM_ROOT / "environments" / "dev" / "variables.tf",
        TERRAFORM_ROOT / "environments" / "dev" / "terraform.tfvars.example",
        TERRAFORM_ROOT / "modules" / "networking" / "variables.tf",
        TERRAFORM_ROOT / "modules" / "networking" / "outputs.tf",
        TERRAFORM_ROOT / "modules" / "storage" / "variables.tf",
        TERRAFORM_ROOT / "modules" / "storage" / "outputs.tf",
        TERRAFORM_ROOT / "modules" / "dns" / "variables.tf",
        TERRAFORM_ROOT / "modules" / "dns" / "outputs.tf",
        TERRAFORM_ROOT / "modules" / "identity" / "variables.tf",
        TERRAFORM_ROOT / "modules" / "identity" / "outputs.tf",
        TERRAFORM_ROOT / "modules" / "cluster" / "variables.tf",
        TERRAFORM_ROOT / "modules" / "cluster" / "outputs.tf",
    )

    missing_paths = [path for path in expected_paths if not path.exists()]
    assert missing_paths == []


def test_terraform_environment_wires_every_required_provider_neutral_module() -> None:
    """The dev blueprint should wire all required module boundaries explicitly."""
    environment_main = (TERRAFORM_ROOT / "environments" / "dev" / "main.tf").read_text(
        encoding="utf-8"
    )

    assert 'module "networking"' in environment_main
    assert 'module "storage"' in environment_main
    assert 'module "dns"' in environment_main
    assert 'module "identity"' in environment_main
    assert 'module "cluster"' in environment_main
    assert "stateful_ssd" in environment_main
    assert "gpu_scratch" in environment_main


def test_terraform_baseline_remains_provider_neutral() -> None:
    """Provider-specific resource types must not appear before OQ-01 narrows."""
    terraform_files = sorted(TERRAFORM_ROOT.rglob("*.tf"))
    terraform_source = "\n".join(
        terraform_file.read_text(encoding="utf-8") for terraform_file in terraform_files
    )

    disallowed_tokens = (
        'resource "aws_',
        'resource "azurerm_',
        'resource "google_',
        'resource "oci_',
        'resource "alicloud_',
        'resource "digitalocean_',
        'resource "linode_',
        'provider "aws"',
        'provider "azurerm"',
        'provider "google"',
        'provider "oci"',
        'provider "alicloud"',
        'provider "digitalocean"',
        'provider "linode"',
    )

    for token in disallowed_tokens:
        assert token not in terraform_source


def test_helm_foundation_chart_exists_with_required_templates_and_schema() -> None:
    """The Helm baseline should publish namespaces, priorities, and a values schema."""
    expected_paths = (
        HELM_ROOT / "Chart.yaml",
        HELM_ROOT / "values.yaml",
        HELM_ROOT / "values.schema.json",
        HELM_ROOT / "templates" / "namespaces.yaml",
        HELM_ROOT / "templates" / "priorityclasses.yaml",
    )

    missing_paths = [path for path in expected_paths if not path.exists()]
    assert missing_paths == []


def test_local_kind_dev_target_exists_with_expected_inputs() -> None:
    """The internal-only local dev target should be defined explicitly."""
    expected_paths = (
        KIND_ROOT / "README.md",
        KIND_ROOT / "dev-cluster.yaml",
        HELM_ROOT / "values.kind-dev.yaml",
    )

    missing_paths = [path for path in expected_paths if not path.exists()]
    assert missing_paths == []


def test_helm_values_schema_requires_namespace_and_storage_alias_contracts() -> None:
    """The chart schema should lock the provider-neutral contract shape."""
    values_schema = json.loads((HELM_ROOT / "values.schema.json").read_text(encoding="utf-8"))

    assert values_schema["required"] == [
        "namespacePrefix",
        "namespaces",
        "priorityClasses",
        "storageProfileAliases",
    ]
    assert values_schema["properties"]["priorityClasses"]["required"] == [
        "general",
        "stateful",
        "gpu",
    ]
    assert values_schema["properties"]["storageProfileAliases"]["required"] == [
        "general",
        "stateful_ssd",
        "gpu_scratch",
    ]


def test_kind_dev_cluster_encodes_logical_node_pool_roles() -> None:
    """The local cluster should preserve general, stateful, and gpu role intent."""
    cluster_config = (KIND_ROOT / "dev-cluster.yaml").read_text(encoding="utf-8")

    assert "maptheisland.io/nodepool=general" in cluster_config
    assert "maptheisland.io/nodepool=stateful" in cluster_config
    assert "maptheisland.io/nodepool=gpu" in cluster_config
    assert "maptheisland.io/accelerator=true:NoSchedule" in cluster_config


def test_kind_dev_values_bind_local_storage_aliases() -> None:
    """The local Helm values should narrow storage aliases for dev validation only."""
    kind_values = (HELM_ROOT / "values.kind-dev.yaml").read_text(encoding="utf-8")

    assert "namespacePrefix: maptheisland-dev" in kind_values
    assert "general: standard" in kind_values
    assert "stateful_ssd: standard" in kind_values
    assert "gpu_scratch: ephemeral" in kind_values


def test_platform_foundation_docs_and_ci_now_cover_infra_surface() -> None:
    """Infra changes should be documented and watched by CI."""
    implementation_readme = (REPO_ROOT / "docs" / "implementation" / "README.md").read_text(
        encoding="utf-8"
    )
    ci_workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )

    assert "platform-foundation-baseline.md" in implementation_readme
    assert "local-dev-platform-target.md" in implementation_readme
    assert '- "infra/**"' in ci_workflow
