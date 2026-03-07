"""Regression checks for the internal-only P01-T03 control-plane baseline."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITOPS_ROOT = REPO_ROOT / "infra" / "gitops"
VALUES_ROOT = REPO_ROOT / "infra" / "helm" / "values" / "control-plane"
IMPLEMENTATION_DOC = (
    REPO_ROOT / "docs" / "implementation" / "control-plane-gitops-secrets-and-certs-baseline.md"
)


def test_control_plane_baseline_files_exist() -> None:
    """The repo should publish the expected Local control-plane file set."""
    expected_paths = (
        IMPLEMENTATION_DOC,
        GITOPS_ROOT / "README.md",
        GITOPS_ROOT / "bootstrap" / "local" / "project.yaml",
        GITOPS_ROOT / "bootstrap" / "local" / "root-application.yaml",
        GITOPS_ROOT / "applications" / "local" / "control-plane" / "platform-foundation.yaml",
        GITOPS_ROOT / "applications" / "local" / "control-plane" / "argocd-self-manage.yaml",
        GITOPS_ROOT / "applications" / "local" / "control-plane" / "cert-manager.yaml",
        GITOPS_ROOT / "applications" / "local" / "control-plane" / "external-secrets.yaml",
        GITOPS_ROOT / "applications" / "local" / "control-plane" / "vault.yaml",
        GITOPS_ROOT
        / "applications"
        / "local"
        / "control-plane"
        / "sample-secret-consumer.yaml",
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "cluster-secret-store.yaml",
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "cluster-issuer.yaml",
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "externalsecret.yaml",
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "certificate.yaml",
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "deployment.yaml",
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "serviceaccount.yaml",
        VALUES_ROOT / "argocd.local-values.yaml",
        VALUES_ROOT / "external-secrets.local-values.yaml",
        VALUES_ROOT / "vault.local-values.yaml",
        VALUES_ROOT / "cert-manager.local-values.yaml",
    )

    missing_paths = [path for path in expected_paths if not path.exists()]
    assert missing_paths == []


def test_control_plane_docs_keep_the_local_only_boundary_explicit() -> None:
    """The implementation doc should preserve the Local-only guardrails."""
    baseline_doc = IMPLEMENTATION_DOC.read_text(encoding="utf-8")

    assert "Local" in baseline_doc
    assert "not authoritative for" in baseline_doc
    assert ".state/kind/vault-root-token" in baseline_doc
    assert "Git reconciliation" in baseline_doc
    assert "not committed to Git" in baseline_doc
    assert "pnpm apply:kind:argocd:gitops" in baseline_doc
    assert "pnpm check:kind:argocd:remote-reconciliation" in baseline_doc


def test_argocd_manifests_pin_repo_and_chart_sources() -> None:
    """The GitOps baseline should pin the repo URL, branch, and chart versions."""
    root_application = (
        GITOPS_ROOT / "bootstrap" / "local" / "root-application.yaml"
    ).read_text(encoding="utf-8")
    project_manifest = (GITOPS_ROOT / "bootstrap" / "local" / "project.yaml").read_text(
        encoding="utf-8"
    )
    argocd_app = (
        GITOPS_ROOT / "applications" / "local" / "control-plane" / "argocd-self-manage.yaml"
    ).read_text(encoding="utf-8")

    assert "https://github.com/bcdannyboy/MapTheIsland.git" in root_application
    assert "targetRevision: main" in root_application
    assert "path: infra/gitops/applications/local/control-plane" in root_application
    assert "https://argoproj.github.io/argo-helm" in project_manifest
    assert "https://charts.external-secrets.io" in project_manifest
    assert "https://helm.releases.hashicorp.com" in project_manifest
    assert "https://charts.jetstack.io" in project_manifest
    assert "namespace: kube-system" in project_manifest
    assert "targetRevision: 9.4.7" in argocd_app
    assert "$values/infra/helm/values/control-plane/argocd.local-values.yaml" in argocd_app


def test_gitops_readme_describes_tracked_remote_validation_commands() -> None:
    """The GitOps README should distinguish remote reconciliation from direct bootstrap."""
    readme = (GITOPS_ROOT / "README.md").read_text(encoding="utf-8")

    assert "pnpm apply:kind:argocd:gitops" in readme
    assert "pnpm check:kind:argocd:remote-reconciliation" in readme
    assert "tracked remote branch" in readme


def test_sample_secret_consumer_path_preserves_namespace_scoping() -> None:
    """Sample resources should keep operators and runtime secrets properly separated."""
    cluster_secret_store = (
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "cluster-secret-store.yaml"
    ).read_text(encoding="utf-8")
    external_secret = (
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "externalsecret.yaml"
    ).read_text(encoding="utf-8")
    certificate = (
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "certificate.yaml"
    ).read_text(encoding="utf-8")
    deployment = (
        GITOPS_ROOT / "apps" / "local" / "sample-secret-consumer" / "deployment.yaml"
    ).read_text(encoding="utf-8")

    assert "namespace: maptheisland-dev-foundation-system" in cluster_secret_store
    assert "namespace: maptheisland-dev-application" in external_secret
    assert "maptheisland-local-sample-runtime" in external_secret
    assert "ClusterSecretStore" in external_secret
    assert "deletionPolicy: Retain" in external_secret
    assert "engineVersion: v2" in external_secret
    assert "mergePolicy: Replace" in external_secret
    assert "conversionStrategy: Default" in external_secret
    assert "decodingStrategy: None" in external_secret
    assert "metadataPolicy: None" in external_secret
    assert "maptheisland-local-selfsigned" in certificate
    assert "secretName: maptheisland-local-sample-tls" in certificate
    assert "secretKeyRef" in deployment
    assert "maptheisland-local-sample-runtime" in deployment
    assert "maptheisland-local-sample-tls" in deployment
