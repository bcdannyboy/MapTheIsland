variable "environment_name" {
  description = "Stable environment identifier."
  type        = string
  default     = "dev"
}

variable "namespace_prefix" {
  description = "Prefix used for foundation namespaces."
  type        = string
  default     = "maptheisland"
}

variable "kubernetes_version" {
  description = "Logical Kubernetes version target for the baseline."
  type        = string
  default     = "1.30"
}
