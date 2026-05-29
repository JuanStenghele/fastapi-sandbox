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

resource "aws_ssm_parameter" "grafana_admin_password" {
  name  = "/${var.app_name}/grafana/password"
  type  = "SecureString"
  value = random_password.grafana.result
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
