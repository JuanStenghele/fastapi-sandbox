output "hosted_zone_name_servers" {
  description = "AWS name servers for the domain"
  value       = aws_route53_zone.main.name_servers
}

output "application_url" {
  description = "URL to access fastapi-sandbox application"
  value       = "http://${var.fastapi_sandbox_subdomain_name}.${var.main_domain_name}"
}

output "load_balancer_hostname" {
  description = "Load balancer hostname from Kubernetes service"
  value       = data.kubernetes_service.fastapi_sandbox_service.status[0].load_balancer[0].ingress[0].hostname
}
