output "blueprint" {
  description = "Provider-neutral storage blueprint and logical storage aliases."
  value = {
    environment_name        = var.environment_name
    object_store_namespace  = var.object_store_namespace
    data_lake_branching     = var.data_lake_branching_enabled
    storage_profile_aliases = var.storage_profile_aliases
    backup_mode             = var.backup_mode
  }
}
