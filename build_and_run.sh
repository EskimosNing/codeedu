#!/bin/bash

APP_NAME="crewai-backend"
PORT=5000

echo "Building Docker image..."
docker build -t $APP_NAME .

echo "Removing old container (if exists)..."
docker rm -f $APP_NAME-running 2>/dev/null || true

echo "Running new container..."
docker run -d \
  --name $APP_NAME-running \
  -p $PORT:5000 \
  -e PROJECT_ROOT="/app/src/codeedu" \
  $APP_NAME

echo "Server running at http://localhost:$PORT"
