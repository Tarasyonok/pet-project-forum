#!/bin/bash

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_PASSWORD="${POSTGRES_PASSWORD}"
DB_NAME="${POSTGRES_DB:-railway}"
TIMEOUT=60

echo "Waiting for database at $DB_HOST:$DB_PORT..."

counter=0
until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  sleep 2
  counter=$((counter + 1))
  echo "Attempt $counter: Waiting for database connection..."
  if [ $counter -ge $TIMEOUT ]; then
    echo "Error: Cannot connect to database at $DB_HOST:$DB_PORT after $TIMEOUT seconds"
    exit 1
  fi
done

echo "Database connection established successfully!"

# Run migrations
python django_forum/manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python django_forum/manage.py shell

# Collect static files
python django_forum/manage.py collectstatic --noinput

echo "All setup tasks completed!"

exec "$@"
