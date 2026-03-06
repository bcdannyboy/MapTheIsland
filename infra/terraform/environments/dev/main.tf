module "networking" {
  source = "../../modules/networking"

  environment_name         = var.environment_name
  network_cidr             = "10.42.0.0/16"
  private_service_cidrs    = ["10.42.10.0/24", "10.42.20.0/24", "10.42.30.0/24"]
  internal_ingress_enabled = true
  egress_mode              = "controlled"
}

module "storage" {
  source = "../../modules/storage"

  environment_name            = var.environment_name
  object_store_namespace      = "${var.environment_name}-maptheisland"
  data_lake_branching_enabled = true
  backup_mode                 = "off-cluster"
  storage_profile_aliases = {
    general = {
      intended_workloads = ["shared-services", "lightweight-queues"]
      persistence_class  = "persistent"
      performance_tier   = "standard"
    }
    stateful_ssd = {
      intended_workloads = ["postgresql", "kafka", "opensearch", "neo4j"]
      persistence_class  = "persistent"
      performance_tier   = "ssd"
    }
    gpu_scratch = {
      intended_workloads = ["ocr", "embeddings", "rerank-experiments"]
      persistence_class  = "ephemeral"
      performance_tier   = "throughput"
    }
  }
}

module "dns" {
  source = "../../modules/dns"

  environment_name           = var.environment_name
  base_domain                = "dev.maptheisland.internal"
  service_subdomain          = "svc"
  external_endpoints_enabled = false
}

module "identity" {
  source = "../../modules/identity"

  environment_name       = var.environment_name
  secrets_system         = "vault_external_secrets"
  workload_identity_mode = "service-scoped"
  namespace_service_accounts = {
    foundation-system = ["external-secrets", "cert-manager", "argocd"]
    ingest            = ["harvester", "docproc", "ocr"]
    review            = ["review-api"]
    retrieval         = ["indexer", "graph-builder", "topics"]
    application       = ["bff", "qa-orchestrator"]
  }
}

module "cluster" {
  source = "../../modules/cluster"

  environment_name       = var.environment_name
  kubernetes_version     = var.kubernetes_version
  namespace_prefix       = var.namespace_prefix
  control_plane_exposure = "private"
  node_pools = {
    general = {
      purpose               = "apis, orchestration, indexing, and lightweight nlp"
      min_count             = 1
      max_count             = 3
      storage_profile_alias = "general"
      accelerator_enabled   = false
    }
    stateful = {
      purpose               = "databases, brokers, and catalog services"
      min_count             = 1
      max_count             = 3
      storage_profile_alias = "stateful_ssd"
      accelerator_enabled   = false
    }
    gpu = {
      purpose               = "ocr recovery, embeddings, reranking, and hosted models"
      min_count             = 0
      max_count             = 2
      storage_profile_alias = "gpu_scratch"
      accelerator_enabled   = true
    }
  }
}
