# GitHub Actions
resource "aws_ssm_parameter" "github_actions_role_arn" {
  name  = "/${var.app_name}/github-actions/role-arn"
  type  = "String"
  value = aws_iam_role.github_actions.arn

  tags = local.app_registry_tags
}

# S3
resource "aws_ssm_parameter" "s3_bucket_name" {
  name  = "/${var.app_name}/s3/bucket_name"
  type  = "String"
  value = aws_s3_bucket.main.bucket

  tags = local.app_registry_tags
}

# Domain
resource "aws_ssm_parameter" "domain" {
  name  = "/${var.app_name}/domain"
  type  = "String"
  value = "${var.fastapi_sandbox_subdomain_name}.${var.main_domain_name}"

  tags = local.app_registry_tags
}

# Subdomains
resource "aws_ssm_parameter" "api_subdomain" {
  name  = "/${var.app_name}/subdomains/api"
  type  = "String"
  value = var.api_subdomain_name

  tags = local.app_registry_tags
}

# Supabase
resource "aws_ssm_parameter" "supabase_host" {
  name  = "/${var.app_name}/supabase/host"
  type  = "String"
  value = var.supabase_host

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "supabase_port" {
  name  = "/${var.app_name}/supabase/port"
  type  = "String"
  value = var.supabase_port

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "supabase_db" {
  name  = "/${var.app_name}/supabase/db"
  type  = "String"
  value = var.supabase_db

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "supabase_user" {
  name  = "/${var.app_name}/supabase/user"
  type  = "String"
  value = var.supabase_user

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "supabase_password" {
  name  = "/${var.app_name}/supabase/password"
  type  = "SecureString"
  value = var.supabase_password

  tags = local.app_registry_tags
}

# Auth
resource "aws_ssm_parameter" "auth_issuer" {
  name  = "/${var.app_name}/auth/issuer"
  type  = "String"
  value = var.auth_issuer

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "auth_audience" {
  name  = "/${var.app_name}/auth/audience"
  type  = "String"
  value = var.auth_audience

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "auth_jwks_uri" {
  name  = "/${var.app_name}/auth/jwks_uri"
  type  = "String"
  value = var.auth_jwks_uri

  tags = local.app_registry_tags
}

# Observability
resource "aws_ssm_parameter" "otel_otlp_endpoint" {
  name  = "/${var.app_name}/otel/otlp_endpoint"
  type  = "String"
  value = var.otel_otlp_endpoint

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "otel_otlp_instance_id" {
  name  = "/${var.app_name}/otel/otlp_instance_id"
  type  = "String"
  value = var.otel_otlp_instance_id

  tags = local.app_registry_tags
}

resource "aws_ssm_parameter" "otel_otlp_token" {
  name  = "/${var.app_name}/otel/otlp_token"
  type  = "SecureString"
  value = var.otel_otlp_token

  tags = local.app_registry_tags
}
