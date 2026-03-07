"""Regression checks for root workspace metadata, scripts, and ignore rules."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_JSON_PATH = REPO_ROOT / "package.json"
GITIGNORE_PATH = REPO_ROOT / ".gitignore"


def test_root_workspace_metadata_reflects_phase_01_state() -> None:
    """The root workspace metadata should no longer describe a Phase 00-only repo."""
    package_json = json.loads(PACKAGE_JSON_PATH.read_text(encoding="utf-8"))

    assert package_json["version"] == "0.1.0-phase-01"
    assert "Phase 01" in package_json["description"]


def test_root_workspace_publishes_infra_and_local_dev_commands() -> None:
    """The root package scripts should expose the current infra validation path."""
    package_json = json.loads(PACKAGE_JSON_PATH.read_text(encoding="utf-8"))
    scripts = package_json["scripts"]

    assert "helm repo add argo https://argoproj.github.io/argo-helm" in scripts["setup:helm:repos"]
    assert scripts["lint:tf"] == "terraform fmt -check -recursive infra/terraform"
    assert "terraform -chdir=infra/terraform/environments/dev init -backend=false" in scripts[
        "validate:tf:dev"
    ]
    assert "TF_DATA_DIR=$PWD/.terraform-cache/dev" in scripts["validate:tf:dev"]
    assert scripts["lint:helm"].startswith("helm lint infra/helm/charts/platform-foundation")
    assert "helm template maptheisland-platform infra/helm/charts/platform-foundation" in scripts[
        "template:helm:kind-dev"
    ]
    assert "pnpm lint:tf" in scripts["check:infra"]
    assert "pnpm validate:tf:dev" in scripts["check:infra"]
    assert "pnpm lint:helm" in scripts["check:infra"]
    assert "pnpm template:helm:kind-dev" in scripts["check:infra"]
    assert scripts["check:control-plane"].startswith("pnpm setup:helm:repos")
    assert "pnpm template:argocd:local" in scripts["check:control-plane"]
    assert "pnpm template:external-secrets:local" in scripts["check:control-plane"]
    assert "pnpm template:vault:local" in scripts["check:control-plane"]
    assert "pnpm template:cert-manager:local" in scripts["check:control-plane"]
    assert "kind create cluster --name maptheisland-dev" in scripts["create:kind:dev"]
    assert "--kubeconfig .state/kind/kubeconfig" in scripts["create:kind:dev"]
    assert "kind delete cluster --name maptheisland-dev" in scripts["delete:kind:dev"]
    assert "rm -f .state/kind/kubeconfig" in scripts["delete:kind:dev"]
    assert "helm upgrade --install maptheisland-platform" in scripts["apply:kind:foundation"]
    assert "kubectl wait --for=condition=Ready nodes --all --timeout=120s" in scripts[
        "check:kind:nodes"
    ]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["check:kind:nodes"]
    assert "kubectl get nodes -L maptheisland.io/nodepool" in scripts["check:kind:nodes"]
    assert "kubectl apply --dry-run=server" in scripts["check:kind:foundation"]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["check:kind:foundation"]
    assert "helm upgrade --install maptheisland-argocd" in scripts["apply:kind:argocd"]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["apply:kind:argocd"]
    assert "kubectl apply --dry-run=server -f infra/gitops/bootstrap/local" in scripts[
        "check:kind:argocd:bootstrap"
    ]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["check:kind:argocd:bootstrap"]
    assert "kubectl apply -f infra/gitops/bootstrap/local" in scripts["apply:kind:argocd:gitops"]
    assert "rollout status statefulset/maptheisland-argocd-application-controller" in scripts[
        "apply:kind:argocd:gitops"
    ]
    assert "Expected revision $EXPECTED_REVISION not reported for $APP" in scripts[
        "check:kind:argocd:remote-reconciliation"
    ]
    assert "wait_app_synced maptheisland-local-bootstrap" in scripts[
        "check:kind:argocd:remote-reconciliation"
    ]
    assert "wait_app_healthy maptheisland-local-bootstrap" in scripts[
        "check:kind:argocd:remote-reconciliation"
    ]
    refresh_command = (
        "annotate application maptheisland-local-bootstrap "
        "argocd.argoproj.io/refresh=hard --overwrite"
    )
    assert refresh_command in scripts["check:kind:argocd:remote-reconciliation"]
    assert "wait_revision maptheisland-local-sample-secret-consumer" in scripts[
        "check:kind:argocd:remote-reconciliation"
    ]
    assert "rollout status statefulset/maptheisland-argocd-application-controller" in scripts[
        "check:kind:argocd:remote-reconciliation"
    ]
    assert "KC=$PWD/.state/kind/kubeconfig" in scripts["check:kind:argocd:remote-reconciliation"]
    assert ".state/kind/vault-root-token" in scripts["bootstrap:kind:vault:token"]
    assert "helm upgrade --install maptheisland-vault" in scripts["apply:kind:vault"]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["apply:kind:vault"]
    assert "exec $POD -- sh -c" in scripts["bootstrap:kind:vault:sample-secret"]
    assert "KC=$PWD/.state/kind/kubeconfig" in scripts["bootstrap:kind:vault:sample-secret"]
    assert "deployment/maptheisland-cert-manager-webhook" in scripts[
        "apply:kind:sample-secret-consumer"
    ]
    assert "deployment/maptheisland-external-secrets-webhook" in scripts[
        "apply:kind:sample-secret-consumer"
    ]
    assert "kubectl apply -f infra/gitops/apps/local/sample-secret-consumer" in scripts[
        "apply:kind:sample-secret-consumer"
    ]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["apply:kind:sample-secret-consumer"]
    assert "certificate/maptheisland-local-sample-certificate" in scripts[
        "check:kind:sample-secret-consumer"
    ]
    assert "KUBECONFIG=$PWD/.state/kind/kubeconfig" in scripts["check:kind:sample-secret-consumer"]


def test_gitignore_covers_current_generated_artifact_classes() -> None:
    """Generated infra and frontend artifacts should be ignored explicitly."""
    gitignore = GITIGNORE_PATH.read_text(encoding="utf-8")

    assert ".terraform/" in gitignore
    assert ".terraform-cache/" in gitignore
    assert ".state/" in gitignore
    assert "*.egg-info/" in gitignore
    assert "apps/web/coverage/" in gitignore
    assert "**/coverage/" in gitignore
    assert "*.tsbuildinfo" in gitignore
