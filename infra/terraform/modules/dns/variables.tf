variable "environment_name" {
  description = "Stable environment identifier such as dev or staging."
  type        = string
}

variable "base_domain" {
  description = "Logical base domain for the environment."
  type        = string
}

variable "service_subdomain" {
  description = "Subdomain used for internal service endpoints."
  type        = string
}

variable "external_endpoints_enabled" {
  description = "Whether external analyst-facing endpoints are expected."
  type        = bool
}
