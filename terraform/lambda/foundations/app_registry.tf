resource "aws_servicecatalogappregistry_application" "main" {
  name = var.app_name
}

locals {
  app_registry_tags = {
    awsApplication    = aws_servicecatalogappregistry_application.main.id
    awsApplicationArn = aws_servicecatalogappregistry_application.main.arn
  }
}
