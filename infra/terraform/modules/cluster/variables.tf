variable "environment_name" {
  description = "Stable environment identifier such as dev or staging."
  type        = string
}

variable "kubernetes_version" {
  description = "Logical Kubernetes version target for the environment."
  type        = string
}

variable "namespace_prefix" {
  description = "Prefix used for chart-rendered namespaces."
  type        = string
}

variable "node_pools" {
  description = "Logical node-pool contracts for general, stateful, and GPU workloads."
  type = map(object({
    purpose               = string
    min_count             = number
    max_count             = number
    storage_profile_alias = string
    accelerator_enabled   = bool
  }))
}

variable "control_plane_exposure" {
  description = "High-level control-plane exposure mode."
  type        = string
}
