#!/bin/bash
set -e

if [ ! -f "/app/data/fp_growth_mba.db" ]; then
    echo "Creating SQLite DB..."
    sqlite3 /app/data/fp_growth_mba.db "VACUUM;"
fi

# Run backend server
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
