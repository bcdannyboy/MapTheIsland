output "blueprint" {
  description = "Provider-neutral identity and secret-delivery blueprint."
  value = {
    environment_name           = var.environment_name
    secrets_system             = var.secrets_system
    namespace_service_accounts = var.namespace_service_accounts
    workload_identity_mode     = var.workload_identity_mode
  }
}
