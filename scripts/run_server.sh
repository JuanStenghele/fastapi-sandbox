#!/bin/bash

if [ "$ENV" = "test" ] || [ "$ENV" = "local" ]; then
  echo "Starting application with development mode..."
  RELOAD="--reload"
else
  echo "Starting application with production mode..."
  RELOAD=""
fi

exec uvicorn main:app --factory --app-dir /fastapi-sandbox/src --host 0.0.0.0 --port ${PORT:-8000} $RELOAD
