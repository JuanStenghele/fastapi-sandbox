resource "aws_iam_policy" "eso" {
  name = "${var.app_name}-eso-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ssm:GetParameter", "ssm:GetParameters", "ssm:GetParametersByPath"]
        Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/${var.app_name}/*"
      }
    ]
  })
}

module "irsa_eso" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version = "5.39.0"

  create_role                   = true
  role_name                     = "${var.app_name}-eso-role"
  provider_url                  = module.eks.oidc_provider
  role_policy_arns              = [aws_iam_policy.eso.arn]
  oidc_fully_qualified_subjects = ["system:serviceaccount:external-secrets:external-secrets"]
}
