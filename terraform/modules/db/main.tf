resource "aws_db_instance" "microservice_db" {
  allocated_storage    = 20 # Free tier
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro" # Free tier
  db_name              = var.db_name
  username             = var.db_user
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
}
