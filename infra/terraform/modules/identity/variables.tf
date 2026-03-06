variable "environment_name" {
  description = "Stable environment identifier such as dev or staging."
  type        = string
}

variable "secrets_system" {
  description = "Logical secret-system contract for the environment."
  type        = string
}

variable "namespace_service_accounts" {
  description = "Namespace-to-service-account map for least-privilege planning."
  type        = map(list(string))
}

variable "workload_identity_mode" {
  description = "Provider-neutral workload identity posture."
  type        = string
}
