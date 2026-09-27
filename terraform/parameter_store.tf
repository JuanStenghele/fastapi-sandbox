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

resource "aws_ssm_parameter" "s3_iam_role_arn" {
  name  = "/${var.app_name}/s3/iam_role_arn"
  type  = "String"
  value = module.irsa_s3.iam_role_arn
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
