#!/bin/bash

if [ "$ENV" = "test" ] || [ "$ENV" = "local" ]; then
  echo "Starting application with fastapi development mode..."
  MODE="dev"
else
  echo "Starting application with fastapi production mode..."
  MODE="run"
fi

exec fastapi $MODE /fastapi-sandbox/src/main.py --port ${PORT:-8000} --host 0.0.0.0
