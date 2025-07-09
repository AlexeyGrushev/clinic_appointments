#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL is available - running migrations..."
python3 -m alembic upgrade head

echo "Starting FastAPI app..."
exec python3 main.py
