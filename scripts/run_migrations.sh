#!/bin/bash
set -e

RETRIES=${DB_MIGRATION_RETRIES:-10}
SLEEP_INTERVAL=${DB_MIGRATION_SLEEP:-3}
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
REQUIRED_VARS=("POSTGRES_HOST" "POSTGRES_PORT" "POSTGRES_USER" "POSTGRES_DB")
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    log_error "Required environment variable $var is not set"
    exit 1
  fi
done

# Function to check database readiness
check_database() {
  pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1
}

log "Checking database readiness..."
COUNT=0
until check_database; do
  COUNT=$((COUNT + 1))
  if [ $COUNT -gt $RETRIES ]; then
    log_error "Database not ready after $RETRIES attempts (${TIMEOUT_TOTAL}s)"
    exit 1
  fi
  log "Waiting for database... (attempt $COUNT/$RETRIES)"
  sleep $SLEEP_INTERVAL
done

log_success "Database is ready"

# Run Alembic migrations
log "Running Alembic migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
  log_success "Migrations completed successfully"
  exit 0
else
  log_error "Migrations failed"
  exit 1
fi
