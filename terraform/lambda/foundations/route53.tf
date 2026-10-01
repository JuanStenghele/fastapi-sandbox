resource "aws_route53_zone" "main" {
  name = var.main_domain_name

  tags = local.app_registry_tags
}
