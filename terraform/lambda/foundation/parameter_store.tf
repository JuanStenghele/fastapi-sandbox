resource "aws_ssm_parameter" "app_registry_id" {
  name  = "/${var.app_name}/app-registry/id"
  type  = "String"
  value = aws_servicecatalogappregistry_application.main.id
}

resource "aws_ssm_parameter" "app_registry_arn" {
  name  = "/${var.app_name}/app-registry/arn"
  type  = "String"
  value = aws_servicecatalogappregistry_application.main.arn
}
