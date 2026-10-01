resource "aws_iam_role" "lambda" {
  name = "${var.app_name}-lambda"

  tags = local.app_registry_tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda" {
  name = "${var.app_name}-github-actions"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["ecr:GetAuthorizationToken"],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        Resource = data.aws_ecr_repository.ecr.arn
      }
    ]
  })
}

resource "aws_lambda_function" "lambda" {
  function_name = "${var.app_name}-lambda"
  role          = aws_iam_role.lambda.arn
  package_type  = "Image"
  image_uri     = "${data.aws_ecr_repository.ecr.repository_url}:latest"

  memory_size = 512
  timeout     = 120

  architectures = ["arm64"] # Graviton support for better price/performance

  tags = local.app_registry_tags

  environment {
    variables = local.lambda_environment
  }
}
