#!/usr/bin/env bash
set -euo pipefail

APP_NAME="juans-fastapi-sandbox"

ssm() { aws ssm get-parameter --name "/${APP_NAME}/$1" ${2:+--with-decryption} --query "Parameter.Value" --output text; }

S3_ROLE_ARN=$(ssm "s3/iam_role_arn")
LETSENCRYPT_EMAIL=$(ssm "letsencrypt/email" true)
ESO_ROLE_ARN=$(ssm "eso/iam_role_arn")
DOMAIN=$(ssm "domain")
API_SUBDOMAIN=$(ssm "subdomains/api")
HEADLAMP_SUBDOMAIN=$(ssm "subdomains/headlamp")
GRAFANA_SUBDOMAIN=$(ssm "subdomains/grafana")

helm upgrade --install fastapi-sandbox helm/ \
  -f helm/values.yaml \
  -f helm/values.prod.yaml \
  -f helm/values.traefik.yaml \
  -f helm/values.eso.yaml \
  --set s3.roleArn="$S3_ROLE_ARN" \
  --set "traefik.certificatesResolvers.letsencrypt.acme.email=$LETSENCRYPT_EMAIL" \
  --set "external-secrets.serviceAccount.annotations.eks\.amazonaws\.com/role-arn=$ESO_ROLE_ARN" \
  --set ingress.domain="$DOMAIN" \
  --set "ingress.subdomains.api=$API_SUBDOMAIN" \
  --set "ingress.subdomains.headlamp=$HEADLAMP_SUBDOMAIN" \
  --set "ingress.subdomains.grafana=$GRAFANA_SUBDOMAIN" \
  --set env.STORAGE_PUBLIC_URL="https://${API_SUBDOMAIN}.${DOMAIN}/storage" \
  --wait --timeout 5m
