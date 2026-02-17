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

# Route 53
variable "main_domain_name" {
  description = "Kubernetes app domain name"
  type        = string
  default     = "25101999.xyz"
}

variable "fastapi_sandbox_subdomain_name" {
  description = "Subdomain for the fastapi-sandbox service"
  type        = string
  default     = "juans-fastapi-sandbox"
}
