output "database_host" {
  value       = module.db.database_host
  description = "El host de la base de datos."
}

output "database_port" {
  value       = module.db.database_port
  description = "El puerto de la base de datos."
}
