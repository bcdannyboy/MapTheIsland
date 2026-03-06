variable "environment_name" {
  description = "Stable environment identifier such as dev or staging."
  type        = string
}

variable "object_store_namespace" {
  description = "Logical namespace for object-store buckets and evidence paths."
  type        = string
}

variable "data_lake_branching_enabled" {
  description = "Whether lakeFS-style branching is required for this environment."
  type        = bool
}

variable "storage_profile_aliases" {
  description = "Logical storage profiles to be mapped to provider-specific classes later."
  type = map(object({
    intended_workloads = list(string)
    persistence_class  = string
    performance_tier   = string
  }))
}

variable "backup_mode" {
  description = "Provider-neutral backup posture for persistent state."
  type        = string
}
