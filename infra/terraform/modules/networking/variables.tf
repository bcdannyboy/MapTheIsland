variable "environment_name" {
  description = "Stable environment identifier such as dev or staging."
  type        = string
}

variable "network_cidr" {
  description = "Provider-neutral primary CIDR for the environment."
  type        = string
}

variable "private_service_cidrs" {
  description = "CIDRs reserved for internal platform services."
  type        = list(string)
}

variable "internal_ingress_enabled" {
  description = "Whether the environment should expose internal ingress paths."
  type        = bool
}

variable "egress_mode" {
  description = "High-level egress posture rather than provider-specific rules."
  type        = string
}
