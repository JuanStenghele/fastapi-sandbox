resource "aws_resourcegroups_group" "main" {
  name        = var.app_name
  description = "Resource group for ${var.app_name}"

  resource_query {
    type = "TAG_FILTERS_1_0"

    query = jsonencode({
      ResourceTypeFilters = ["AWS::AllSupported"]
      TagFilters = [{
        Key    = "awsApplication"
        Values = [var.app_name]
      }]
    })
  }
}

locals {
  app_registry_tags = {
    awsApplication = var.app_name
  }
}
