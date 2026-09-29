locals {
  # Grafana Cloud OTLP auth header: "Basic <base64(instanceId:token)>"
  otel_otlp_auth = "Basic ${base64encode("${aws_ssm_parameter.otel_otlp_instance_id.value}:${aws_ssm_parameter.otel_otlp_token.value}")}"

  lambda_environment = {
    ENV                         = "production"
    POSTGRES_HOST               = aws_ssm_parameter.supabase_host.value
    POSTGRES_PORT               = aws_ssm_parameter.supabase_port.value
    POSTGRES_DB                 = aws_ssm_parameter.supabase_db.value
    POSTGRES_USER               = aws_ssm_parameter.supabase_user.value
    POSTGRES_PASSWORD           = aws_ssm_parameter.supabase_password.value
    POSTGRES_SSLMODE            = "require"
    STORAGE_BUCKET_NAME         = aws_s3_bucket.main.bucket
    STORAGE_REGION              = var.aws_region
    STORAGE_PUBLIC_URL          = "https://${local.api_domain}"
    AUTH_ISSUER                 = aws_ssm_parameter.auth_issuer.value
    AUTH_AUDIENCE               = aws_ssm_parameter.auth_audience.value
    AUTH_JWKS_URI               = aws_ssm_parameter.auth_jwks_uri.value
    OTEL_EXPORTER_OTLP_ENDPOINT = aws_ssm_parameter.otel_otlp_endpoint.value
    OTEL_EXPORTER_OTLP_AUTH     = local.otel_otlp_auth
    CORS_MIDDLEWARE_ENABLED     = "true"
    CORS_ALLOWED_ORIGINS        = "https://${local.ui_domain}"
  }
}
