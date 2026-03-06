output "foundation_blueprint" {
  description = "Aggregated provider-neutral blueprint for the dev environment."
  value = {
    networking = module.networking.blueprint
    storage    = module.storage.blueprint
    dns        = module.dns.blueprint
    identity   = module.identity.blueprint
    cluster    = module.cluster.blueprint
  }
}
