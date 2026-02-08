variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
  default     = null
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
  default     = null
}

# RDS
variable "rds_username" {
  description = "Username for RDS"
  type        = string
  sensitive   = true
  default     = null
}

variable "rds_password" {
  description = "Password for RDS"
  type        = string
  sensitive   = true
  default     = null
}
