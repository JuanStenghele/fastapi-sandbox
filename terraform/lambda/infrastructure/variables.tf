variable "app_name" {
  description = "Application Name"
  type        = string
  default     = "jstenghele-fastapi-sandbox"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "sa-east-1"
}

# GitHub
variable "github_repo" {
  description = "GitHub repository in the format owner/repo"
  type        = string
  default     = "JuanStenghele/fastapi-sandbox"
}

# S3
variable "s3_bucket_name" {
  description = "Name of the S3 bucket for file storage"
  type        = string
  default     = "fastapi-sandbox-production"
}

# DNS
variable "main_domain_name" {
  description = "Main domain name"
  type        = string
  default     = "25101999.xyz"
}

variable "fastapi_sandbox_subdomain_name" {
  description = "Subdomain for the fastapi-sandbox service"
  type        = string
  default     = "jstenghele-fastapi-sandbox"
}

variable "api_subdomain_name" {
  description = "Subdomain for the API service"
  type        = string
  default     = "api"
}

variable "ui_subdomain_name" {
  description = "Subdomain for the UI service"
  type        = string
  default     = "ui"
}

# Supabase
variable "supabase_host" {
  description = "Supabase database host"
  type        = string
}

variable "supabase_port" {
  description = "Supabase database port"
  type        = string
  default     = "6543"
}

variable "supabase_db" {
  description = "Supabase database name"
  type        = string
  default     = "postgres"
}

variable "supabase_user" {
  description = "Supabase database user"
  type        = string
}

variable "supabase_password" {
  description = "Supabase database password"
  type        = string
  sensitive   = true
}

# Auth
variable "auth_issuer" {
  description = "Auth issuer URL"
  type        = string
}

variable "auth_audience" {
  description = "Auth audience"
  type        = string
}

variable "auth_jwks_uri" {
  description = "Auth JWKS URI"
  type        = string
}

# Observability
variable "otel_otlp_endpoint" {
  description = "OpenTelemetry OTLP endpoint"
  type        = string
}

variable "otel_otlp_instance_id" {
  description = "Grafana Cloud instance ID"
  type        = string
}

variable "otel_otlp_token" {
  description = "Grafana Cloud access policy token"
  type        = string
  sensitive   = true
}
