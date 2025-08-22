#!/usr/bin/env bash
set -e  # có lỗi là dừng

dbt deps  --project-dir /app/fp_growth_mba
dbt seed  --project-dir /app/fp_growth_mba
dbt run   --project-dir /app/fp_growth_mba

exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
