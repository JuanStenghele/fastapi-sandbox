#!/bin/bash

if [ "$ENV" = "dev" ] || [ "$ENV" = "test" ]; then
  echo "Starting application with fastapi development mode..."
  MODE="dev"
else
  echo "Starting application with fastapi production mode..."
  MODE="run"
fi

exec fastapi $MODE /fastapi-sandbox/src/main.py --port 8000 --host 0.0.0.0
