#!/bin/bash

# Use the PUBLIC proxy URL that Railway provides
PUBLIC_HOST="trolley.proxy.rlwy.net"
PUBLIC_PORT="50110"

echo "Using public database endpoint for setup: $PUBLIC_HOST:$PUBLIC_PORT"

# Temporarily override the database connection using environment variables
# These will override what decouple.config() reads
export DB_HOST="$PUBLIC_HOST"
export DB_PORT="$PUBLIC_PORT"

echo "Running database migrations..."
python django_forum/manage.py migrate

echo "Creating superuser if needed..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python django_forum/manage.py shell

echo "Collecting static files..."
python django_forum/manage.py collectstatic --noinput

echo "All setup tasks completed!"

# Reset to internal host for the main application
unset DB_HOST
unset DB_PORT

exec "$@"