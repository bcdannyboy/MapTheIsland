output "blueprint" {
  description = "Provider-neutral networking blueprint for downstream modules."
  value = {
    environment_name         = var.environment_name
    network_cidr             = var.network_cidr
    private_service_cidrs    = var.private_service_cidrs
    internal_ingress_enabled = var.internal_ingress_enabled
    egress_mode              = var.egress_mode
  }
}
