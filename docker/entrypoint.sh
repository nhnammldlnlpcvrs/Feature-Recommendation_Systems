#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

until pg_isready -h db -p 5432 -U postgres > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL is ready. Starting backend..."

exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload