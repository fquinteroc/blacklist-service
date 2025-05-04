# Las llaves estan vacia aqui pero tienen valor en terraform.tfvars (Archivo que debe meterse en el .gitignore)
# aws_access_key = "<my-access-key>"
# aws_secret_key = "<my-secret-key>"

variable "aws_access_key" {}

variable "aws_secret_key" {}

variable "aws_region" {
  type        = string
  description = "La region donde vamos a desplegar la infraestructura"
  default     = "us-east-1"
  nullable    = false
}

variable "app_name" {
  type        = string
  description = "Nombre del microservicio"
  default     = "blacklist-service"
  nullable    = false
}

variable "db_name" {
  type        = string
  description = "Nombre de la base de datos"
  default     = "blacklistdb"
  nullable    = false
}

variable "db_user" {
  type        = string
  description = "Usuario de la base de datos"
  default     = "userdb"
  nullable    = false
}

variable "db_password" {
  type        = string
  description = "Contraseña de la base de datos"
  sensitive   = true
}

variable "deployment_policy" {
  description = "strategia de despliegue (e.g., AllAtOnce, Rolling, RollingWithAdditionalBatch, Immutable, TrafficSplitting)"
  default     = "Rolling"
}
