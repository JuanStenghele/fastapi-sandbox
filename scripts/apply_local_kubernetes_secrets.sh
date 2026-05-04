#!/bin/bash
set -e

if [ ! -f .env ]; then
  echo "ERROR: .env file not found. Copy .env.example to .env and populate it."
  exit 1
fi

set -a
source .env
set +a

for template in helm/secrets/*.template.yaml; do
  envsubst < "$template" | kubectl apply -f -
done
