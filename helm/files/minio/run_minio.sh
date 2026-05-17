#!/bin/bash
set -e

RETRIES=${MINIO_RETRIES:-10}
SLEEP_INTERVAL=${MINIO_SLEEP:-3}
TIMEOUT_TOTAL=$((RETRIES * SLEEP_INTERVAL))

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NO_COLOR='\033[0m' # No Color

# Function to log with timestamp
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Function to log success in green
log_success() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${GREEN}$*${NO_COLOR}"
}

# Function to log error in red
log_error() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${RED}ERROR: $*${NO_COLOR}"
}

# Validate required environment variables
REQUIRED_VARS=("MINIO_ROOT_USER" "MINIO_ROOT_PASSWORD" "STORAGE_BUCKET_NAME")
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    log_error "Required environment variable $var is not set"
    exit 1
  fi
done

MINIO_CONSOLE_PORT=${MINIO_CONSOLE_PORT:-9001}

log "Starting MinIO server..."
minio server /data --console-address ":$MINIO_CONSOLE_PORT" &

# Function to check MinIO readiness
check_minio() {
  mc alias set local http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" > /dev/null 2>&1
}

log "Checking MinIO readiness..."
COUNT=0
until check_minio; do
  COUNT=$((COUNT + 1))
  if [ $COUNT -gt $RETRIES ]; then
    log_error "MinIO not ready after $RETRIES attempts (${TIMEOUT_TOTAL}s)"
    exit 1
  fi
  log "Waiting for MinIO... (attempt $COUNT/$RETRIES)"
  sleep $SLEEP_INTERVAL
done

log_success "MinIO is ready"

log "Creating bucket '$STORAGE_BUCKET_NAME'..."
mc mb --ignore-existing "local/$STORAGE_BUCKET_NAME"
log_success "Bucket '$STORAGE_BUCKET_NAME' ready"

log "Setting all buckets to public (anonymous download)..."
while read -ra fields; do
  bucket="${fields[-1]%/}"
  mc anonymous set download "local/$bucket"
  log_success "Bucket '$bucket' set to public"
done < <(mc ls local)

log_success "All buckets set to public successfully"

wait
