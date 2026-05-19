resource "aws_iam_policy" "s3" {
  name = "${var.app_name}-s3-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "${aws_s3_bucket.main.arn}/public/*"
      }
    ]
  })
}

module "irsa_s3" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version = "5.39.0"

  create_role                   = true
  role_name                     = "${var.app_name}-s3-role"
  provider_url                  = module.eks.oidc_provider
  role_policy_arns              = [aws_iam_policy.s3.arn]
  oidc_fully_qualified_subjects = ["system:serviceaccount:default:fastapi-sandbox-sa"]
}

resource "aws_s3_bucket" "main" {
  bucket = var.s3_bucket_name

  tags = {
    Name = var.s3_bucket_name
  }
}

resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "main" {
  bucket     = aws_s3_bucket.main.id
  depends_on = [aws_s3_bucket_public_access_block.main]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = ["s3:GetObject"]
        Resource  = "${aws_s3_bucket.main.arn}/public/*"
      }
    ]
  })
}
