#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for the database to be ready
echo "Waiting for database to be ready..."
until nc -z db 5432; do
  echo "Database is unavailable - waiting..."
  sleep 1
done
echo "Database is up - continuing..."

# Run database migrations (using Alembic)
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI server
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000