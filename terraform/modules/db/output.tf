output "database_host" {
  value       = aws_db_instance.microservice_db.address
  description = "El host de la base de datos."
}

output "database_port" {
  value       = aws_db_instance.microservice_db.port
  description = "El puerto de la base de datos."
}
