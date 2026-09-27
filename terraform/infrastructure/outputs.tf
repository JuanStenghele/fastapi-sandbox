output "vpc_id" {
  description = "ID of the VPC where the cluster is provisioned"
  value       = module.vpc.vpc_id
}

# S3
output "s3_iam_role_arn" {
  description = "IAM role ARN for the API to access S3 via IRSA"
  value       = module.irsa_s3.iam_role_arn
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.main.bucket
}

output "s3_bucket_arn" {
  description = "S3 bucket ARN"
  value       = aws_s3_bucket.main.arn
}

output "s3_bucket_region" {
  description = "S3 bucket region"
  value       = aws_s3_bucket.main.region
}

# Domain
output "hosted_zone_name_servers" {
  description = "AWS name servers for the domain"
  value       = aws_route53_zone.main.name_servers
}

output "application_url" {
  description = "URL to access the application"
  value       = "https://${local.api_domain}"
}

output "api_gateway_url" {
  description = "API Gateway default URL"
  value       = aws_apigatewayv2_api.main.api_endpoint
}
