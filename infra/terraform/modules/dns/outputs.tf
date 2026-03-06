output "blueprint" {
  description = "Provider-neutral DNS ownership and endpoint-intent blueprint."
  value = {
    environment_name           = var.environment_name
    base_domain                = var.base_domain
    service_subdomain          = var.service_subdomain
    external_endpoints_enabled = var.external_endpoints_enabled
  }
}
