data "aws_ecr_repository" "ecr" {
  name = "${var.app_name}-lambda"
}

data "aws_route53_zone" "main" {
  name = var.main_domain_name
}
