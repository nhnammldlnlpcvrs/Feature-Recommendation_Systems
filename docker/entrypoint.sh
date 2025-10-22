#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

until python -c "import psycopg2; import sys; import time; 
try:
    psycopg2.connect('dbname=fp_growth_mba user=postgres password=abc123 host=db port=5432'); 
    sys.exit(0)
except Exception:
    time.sleep(1)" > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL is ready. Starting backend..."

exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload