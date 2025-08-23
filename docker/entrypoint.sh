set -e

until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Waiting for database $DB_HOST:$DB_PORT..."
  sleep 2
done

echo "Starting backend..."
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
