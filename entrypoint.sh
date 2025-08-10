#!/bin/sh

# Wait for the database to be ready
# This is a simple loop, a more robust solution might use pg_isready
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run database migrations
alembic upgrade head

# Start the main application
exec "$@"
