data "aws_ssm_parameter" "app_registry_id" {
  name = "/${var.app_name}/app-registry/id"
}

data "aws_ssm_parameter" "app_registry_arn" {
  name = "/${var.app_name}/app-registry/arn"
}

locals {
  app_registry_tags = {
    awsApplication    = data.aws_ssm_parameter.app_registry_id.value
    awsApplicationArn = data.aws_ssm_parameter.app_registry_arn.value
  }
}
