resource "aws_ssm_parameter" "ecr_repository_url" {
  name  = "/${var.app_name}/ecr/repository-url"
  type  = "String"
  value = aws_ecr_repository.ecr.repository_url
}

resource "aws_ssm_parameter" "ecr_repository_name" {
  name  = "/${var.app_name}/ecr/repository-name"
  type  = "String"
  value = aws_ecr_repository.ecr.name
}
