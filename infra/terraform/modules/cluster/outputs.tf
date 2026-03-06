output "blueprint" {
  description = "Provider-neutral cluster blueprint and logical node-pool model."
  value = {
    environment_name       = var.environment_name
    kubernetes_version     = var.kubernetes_version
    namespace_prefix       = var.namespace_prefix
    node_pools             = var.node_pools
    control_plane_exposure = var.control_plane_exposure
  }
}
