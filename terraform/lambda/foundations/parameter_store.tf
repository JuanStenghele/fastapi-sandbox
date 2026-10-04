# GitHub Actions
resource "aws_ssm_parameter" "github_actions_role_arn" {
  name  = "/${var.app_name}/github-actions/role-arn"
  type  = "String"
  value = aws_iam_role.github_actions.arn

  tags = local.app_registry_tags
}

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
