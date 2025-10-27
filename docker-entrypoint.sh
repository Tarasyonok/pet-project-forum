#!/bin/bash

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

echo "Waiting for database at $DB_HOST:$DB_PORT..."

counter=0
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
  counter=$((counter + 1))
  if [ $counter -ge 30 ]; then
    echo "Error: Database at $DB_HOST:$DB_PORT not available after 30 seconds"
    exit 1
  fi
done

echo "Database started successfully!"

# Run migrations
python django_forum/manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python django_forum/manage.py shell

# Collect static files
python django_forum/manage.py collectstatic --noinput

echo "All setup tasks completed!"

# Execute the main command (from CMD in Dockerfile)
exec "$@"