#!/bin/bash
set -e

echo "Loading data into online_retail table..."

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy online_retail FROM '/data/online_retail.csv' WITH CSV HEADER DELIMITER ','"