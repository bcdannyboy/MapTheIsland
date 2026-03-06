# Research Register

This register records external sources reviewed for planning. All entries below were verified by browsing official or primary sources on 2026-03-06 unless noted otherwise.

| ID | Source | Type | Why It Matters | Planning Claims Supported |
| --- | --- | --- | --- | --- |
| S-001 | https://www.justice.gov/epstein | official source page | confirms the DOJ corpus is a living public source and frames source acquisition scope | lawful source boundary, incremental harvesting |
| S-002 | https://www.justice.gov/opa/media/1426091/dl | official DOJ memorandum | supports victim-protective review constraints and document rendering caveats | no deanonymization, email rendering caveats, sensitive handling |
| S-003 | https://www.justice.gov/epstein/search | official DOJ search page | supports the claim that official search can be unreliable for some formats | image/native/OCR tri-layer requirement |
| S-004 | https://kubernetes.io/docs/home/ | official documentation | supports Kubernetes as the deployment control plane | cluster baseline, stateful/stateless split |
| S-005 | https://docs.astral.sh/uv/ | official documentation | supports `uv` as the Python project and lockfile manager | toolchain standardization, `uv.lock`, `uv sync`, reproducible Python bootstrap |
| S-006 | https://docs.lakefs.io/ | official documentation | supports branch/merge semantics for data version control | immutable ingest branches, replayability |
| S-007 | https://iceberg.apache.org/spec/ | official specification | supports snapshots, schema evolution, and table semantics | analytical asset strategy |
| S-008 | https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/ | official documentation | supports lexical plus semantic hybrid retrieval | search stack and evidence workbench search behavior |
| S-009 | https://docs.opensearch.org/latest/security/access-control/document-level-security/ | official documentation | supports the operational warning that DLS does not secure write paths | service-only write enforcement |
| S-010 | https://docs.dagster.io/api/dagster/assets | official documentation | supports software-defined asset orchestration | asset lineage and rematerialization model |
| S-011 | https://trino.io/docs/current/connector/iceberg.html | official documentation | supports Trino-over-Iceberg analytical querying | saved analytics and SQL strategy |
| S-012 | https://neo4j.com/docs/cypher-manual/current/introduction/ | official documentation | supports Cypher-based graph querying | graph explorer and graph-service planning |
| S-013 | https://microsoft.github.io/presidio/ | official documentation | supports PII/sensitivity detection strategy | early sensitivity tagging and safety filtering |
| S-014 | https://pypdf.readthedocs.io/en/stable/user/extract-text.html | official documentation | supports native PDF text extraction capabilities | docproc lane and evidence extraction |
| S-015 | https://nextjs.org/docs/app | official documentation | supports Next.js App Router and route model | frontend shell planning |
| S-016 | https://fastapi.tiangolo.com/ | official documentation | supports FastAPI as typed async BFF | BFF planning |
| S-017 | https://mozilla.github.io/pdf.js/ | official documentation | supports browser-side PDF rendering | document viewer planning |
| S-018 | https://tanstack.com/query/latest | official documentation | supports server-state caching/job polling strategy | client state and job management |
| S-019 | https://playwright.dev/docs/intro | official documentation | supports end-to-end workflow testing | release and UI test strategy |
| S-020 | https://www.keycloak.org/securing-apps/oidc-layers | official documentation | supports OIDC-based auth model | auth and access-control plan |
| S-021 | https://agilemanifesto.org/principles.html | primary source | supports iterative, value-focused delivery framing | agile operating model |
| S-022 | https://scrumguides.org/scrum-guide.html | primary source | supports incremental delivery and explicit definitions of done | delivery operating model |
| S-023 | https://kind.sigs.k8s.io/docs/user/quick-start/ | official documentation | supports `kind` as a Docker-backed local self-managed Kubernetes target | internal-only local-dev cluster baseline and bootstrap commands |
| S-024 | https://helm.sh/docs/helm/helm_lint/ | official documentation | supports executable Helm chart linting as part of the local and CI validation surface | infra validation gate for `platform-foundation` |
| S-025 | https://helm.sh/docs/helm/helm_template/ | official documentation | supports Helm render validation before or alongside Kubernetes API checks | rendered-chart validation and `kubectl apply --dry-run=server` flow |
| S-026 | https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/ | official documentation | supports Local Argo CD installation and CRD bootstrap expectations | internal-only `P01-T03-S01` install path |
| S-027 | https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/ | official documentation | supports Argo CD cluster bootstrapping and app-of-apps style repository management | Local GitOps baseline and root-bootstrap manifest design |
| S-028 | https://external-secrets.io/latest/introduction/getting-started/ | official documentation | supports current External Secrets Operator installation and CRD expectations | internal-only `P01-T03-S02` operator baseline |
| S-029 | https://external-secrets.io/latest/provider/hashicorp-vault/ | official documentation | supports Vault-backed External Secrets store configuration | Local Vault plus External Secrets delivery path |
| S-030 | https://developer.hashicorp.com/vault/docs/platform/k8s/helm/run | official documentation | supports Local Vault Helm deployment behavior and the chart-based bootstrap approach | Local Vault baseline and bootstrap-token path |
| S-031 | https://cert-manager.io/docs/installation/helm/ | official documentation | supports current cert-manager Helm installation and CRD handling | internal-only `P01-T03-S03` cert-manager baseline |
| S-032 | https://cert-manager.io/docs/configuration/selfsigned/ | official documentation | supports a self-signed issuer for Local-only certificate validation | Local certificate ownership and sample certificate baseline |

## Use Rule

- New research that changes scope, sequencing, quality gates, or implementation standards must be added here before the plan is updated.
- Secondary sources should be avoided unless no primary source exists.
