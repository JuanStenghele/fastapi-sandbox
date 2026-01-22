output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "vpc_id" {
  description = "ID of the VPC where the cluster is provisioned"
  value       = module.vpc.vpc_id
}

output "configure_kubectl" {
  description = "Configure kubectl: make sure you're logged in with the correct AWS profile and run the following command to update your kubeconfig"
  value       = "aws eks --region us-east-1 update-kubeconfig --name ${var.app_name}-eks"
}

output "hosted_zone_name_servers" {
  description = "AWS name servers for the domain"
  value       = aws_route53_zone.main.name_servers
}

output "application_url" {
  description = "URL to access fastapi-sandbox application"
  value       = "http://${var.fastapi_sandbox_subdomain_name}.${var.main_domain_name}"
}
