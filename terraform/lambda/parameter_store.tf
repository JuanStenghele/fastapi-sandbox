# GitHub Actions
resource "aws_ssm_parameter" "github_actions_role_arn" {
  name  = "/${var.app_name}/github-actions/role-arn"
  type  = "String"
  value = aws_iam_role.github_actions.arn
}

# S3
resource "aws_ssm_parameter" "s3_bucket_name" {
  name  = "/${var.app_name}/s3/bucket_name"
  type  = "String"
  value = aws_s3_bucket.main.bucket
}

# Domain
resource "aws_ssm_parameter" "domain" {
  name  = "/${var.app_name}/domain"
  type  = "String"
  value = "${var.fastapi_sandbox_subdomain_name}.${var.main_domain_name}"
}

# Subdomains
resource "aws_ssm_parameter" "api_subdomain" {
  name  = "/${var.app_name}/subdomains/api"
  type  = "String"
  value = var.api_subdomain_name
}

# Supabase
resource "aws_ssm_parameter" "supabase_host" {
  name  = "/${var.app_name}/supabase/host"
  type  = "String"
  value = var.supabase_host
}

resource "aws_ssm_parameter" "supabase_port" {
  name  = "/${var.app_name}/supabase/port"
  type  = "String"
  value = var.supabase_port
}

resource "aws_ssm_parameter" "supabase_db" {
  name  = "/${var.app_name}/supabase/db"
  type  = "String"
  value = var.supabase_db
}

resource "aws_ssm_parameter" "supabase_user" {
  name  = "/${var.app_name}/supabase/user"
  type  = "String"
  value = var.supabase_user
}

resource "aws_ssm_parameter" "supabase_password" {
  name  = "/${var.app_name}/supabase/password"
  type  = "SecureString"
  value = var.supabase_password
}

# Auth
resource "aws_ssm_parameter" "auth_issuer" {
  name  = "/${var.app_name}/auth/issuer"
  type  = "String"
  value = var.auth_issuer
}

resource "aws_ssm_parameter" "auth_audience" {
  name  = "/${var.app_name}/auth/audience"
  type  = "String"
  value = var.auth_audience
}

resource "aws_ssm_parameter" "auth_jwks_uri" {
  name  = "/${var.app_name}/auth/jwks_uri"
  type  = "String"
  value = var.auth_jwks_uri
}

# Observability
resource "aws_ssm_parameter" "otel_otlp_endpoint" {
  name  = "/${var.app_name}/otel/otlp_endpoint"
  type  = "String"
  value = var.otel_otlp_endpoint
}

resource "aws_ssm_parameter" "otel_otlp_instance_id" {
  name  = "/${var.app_name}/otel/otlp_instance_id"
  type  = "String"
  value = var.otel_otlp_instance_id
}

resource "aws_ssm_parameter" "otel_otlp_token" {
  name  = "/${var.app_name}/otel/otlp_token"
  type  = "SecureString"
  value = var.otel_otlp_token
}
