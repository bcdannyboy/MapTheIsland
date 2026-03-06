"""Regression checks for the repository CI workflow baseline."""

from __future__ import annotations

from pathlib import Path

WORKFLOW_PATH = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml"


def test_ci_workflow_exists_and_targets_repository_change_surfaces() -> None:
    """The Phase 01 CI workflow should watch the current monorepo surfaces."""
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "name: ci" in workflow
    assert 'workflow_dispatch:' in workflow
    assert '- "infra/**"' in workflow
    assert '- "libs/**"' in workflow
    assert '- "apps/**"' in workflow
    assert '- "pyproject.toml"' in workflow


def test_ci_workflow_runs_the_published_python_web_and_infra_quality_gates() -> None:
    """The workflow should run the documented Python, web, and infra gates."""
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "python-validation:" in workflow
    assert "infra-validation:" in workflow
    assert "web-validation:" in workflow
    assert "uv sync --dev" in workflow
    assert "uv run ruff check ." in workflow
    assert "uv run mypy libs/schemas/src libs/contracts/src libs/policy/src tests" in workflow
    assert "uv run pytest" in workflow
    assert "pnpm check:web" in workflow
    assert "pnpm install --frozen-lockfile" in workflow
    assert "terraform fmt -check -recursive infra/terraform" in workflow
    assert "terraform -chdir=infra/terraform/environments/dev init -backend=false" in workflow
    assert "terraform -chdir=infra/terraform/environments/dev validate" in workflow
    assert "TF_DATA_DIR=$PWD/.terraform-cache/dev" in workflow
    assert "azure/setup-helm@v4.3.1" in workflow
    assert "hashicorp/setup-terraform@v4.0.0" in workflow
    assert "helm lint infra/helm/charts/platform-foundation" in workflow
    assert "helm template maptheisland-platform infra/helm/charts/platform-foundation" in workflow
    assert "helm repo add argo https://argoproj.github.io/argo-helm --force-update" in workflow
    assert (
        "helm repo add external-secrets https://charts.external-secrets.io --force-update"
        in workflow
    )
    assert "helm repo add hashicorp https://helm.releases.hashicorp.com --force-update" in workflow
    assert "helm repo add jetstack https://charts.jetstack.io --force-update" in workflow
    assert "helm template maptheisland-argocd argo/argo-cd --version 9.4.7" in workflow
    assert (
        "helm template maptheisland-external-secrets external-secrets/external-secrets "
        "--version 2.0.1" in workflow
    )
    assert "helm template maptheisland-vault hashicorp/vault --version 0.32.0" in workflow
    assert (
        "helm template maptheisland-cert-manager jetstack/cert-manager --version v1.19.4"
        in workflow
    )
