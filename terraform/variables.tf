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

# Ingress
variable "main_domain_name" {
  description = "Main domain name"
  type        = string
  default     = "25101999.xyz"
}

variable "fastapi_sandbox_subdomain_name" {
  description = "Subdomain for the fastapi-sandbox service"
  type        = string
  default     = "juans-fastapi-sandbox"
}

variable "api_subdomain_name" {
  description = "Subdomain for the API service"
  type        = string
  default     = "api"
}
