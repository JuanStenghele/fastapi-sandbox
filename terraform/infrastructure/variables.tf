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
  default     = "juansfastapisandboxdb"
}
