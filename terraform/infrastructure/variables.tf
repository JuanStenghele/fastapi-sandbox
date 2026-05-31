variable "github_repo" {
  description = "GitHub repository in the format owner/repo"
  type        = string
  default     = "JuanStenghele/fastapi-sandbox"
}

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

# S3
variable "s3_bucket_name" {
  description = "Name of the S3 bucket for file storage"
  type        = string
  default     = "fastapi-sandbox-production"
}

# RDS
variable "rds_database_name" {
  description = "Name of the database to create"
  type        = string
  default     = "fastapi_sandbox_db"
}

variable "rds_username" {
  description = "Username for RDS"
  type        = string
  default     = "dev"
}

variable "rds_port" {
  description = "Port for RDS"
  type        = string
  default     = "5432"
}

# Grafana
variable "grafana_admin_user" {
  description = "Grafana admin username"
  type        = string
  default     = "admin"
}

# Let's Encrypt
variable "letsencrypt_email" {
  description = "Email for Let's Encrypt certificate notifications"
  type        = string
  sensitive   = true
}
