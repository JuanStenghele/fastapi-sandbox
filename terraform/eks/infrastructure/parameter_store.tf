# RDS
resource "random_password" "rds" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>?"
}

resource "aws_ssm_parameter" "rds_host" {
  name  = "/${var.app_name}/rds/host"
  type  = "String"
  value = aws_db_instance.main.address
}

resource "aws_ssm_parameter" "rds_port" {
  name  = "/${var.app_name}/rds/port"
  type  = "String"
  value = var.rds_port
}

resource "aws_ssm_parameter" "rds_database_name" {
  name  = "/${var.app_name}/rds/database_name"
  type  = "String"
  value = var.rds_database_name
}

resource "aws_ssm_parameter" "rds_username" {
  name  = "/${var.app_name}/rds/username"
  type  = "String"
  value = var.rds_username
}

resource "aws_ssm_parameter" "rds_password" {
  name  = "/${var.app_name}/rds/password"
  type  = "SecureString"
  value = random_password.rds.result
}

# Grafana
resource "random_password" "grafana" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>?"
}

resource "aws_ssm_parameter" "grafana_admin_user" {
  name  = "/${var.app_name}/grafana/username"
  type  = "String"
  value = var.grafana_admin_user
}

resource "aws_ssm_parameter" "grafana_admin_password" {
  name  = "/${var.app_name}/grafana/password"
  type  = "SecureString"
  value = random_password.grafana.result
}

# GitHub Actions
resource "aws_ssm_parameter" "github_actions_role_arn" {
  name  = "/${var.app_name}/github-actions/role-arn"
  type  = "String"
  value = aws_iam_role.github_actions.arn
}

# ESO
resource "aws_ssm_parameter" "eso_iam_role_arn" {
  name  = "/${var.app_name}/eso/iam_role_arn"
  type  = "String"
  value = module.irsa_eso.iam_role_arn
}

# S3
resource "aws_ssm_parameter" "s3_bucket_name" {
  name  = "/${var.app_name}/s3/bucket_name"
  type  = "String"
  value = aws_s3_bucket.main.bucket
}

resource "aws_ssm_parameter" "s3_iam_role_arn" {
  name  = "/${var.app_name}/s3/iam_role_arn"
  type  = "String"
  value = module.irsa_s3.iam_role_arn
}

# Let's Encrypt
resource "aws_ssm_parameter" "letsencrypt_email" {
  name  = "/${var.app_name}/letsencrypt/email"
  type  = "SecureString"
  value = var.letsencrypt_email
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

resource "aws_ssm_parameter" "headlamp_subdomain" {
  name  = "/${var.app_name}/subdomains/headlamp"
  type  = "String"
  value = var.headlamp_subdomain_name
}

resource "aws_ssm_parameter" "grafana_subdomain" {
  name  = "/${var.app_name}/subdomains/grafana"
  type  = "String"
  value = var.grafana_subdomain_name
}

