variable "app_name" {
  description = "Application Name"
  type        = string
  default     = "juans-fastapi-sandbox"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "sa-east-1"
}

# RDS
variable "rds_database_name" {
  description = "Name of the database to create"
  type        = string
  default     = "juansfastapisandboxdb"
}

variable "rds_username" {
  description = "RDS master username"
  type        = string
  sensitive   = true
}

variable "rds_password" {
  description = "RDS master password"
  type        = string
  sensitive   = true
}
