#!/bin/bash

echo "Waiting for Railway internal DNS to propagate..."
sleep 20

echo "Running database migrations..."
python django_forum/manage.py migrate

echo "Creating superuser if needed..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python django_forum/manage.py shell

echo "Collecting static files..."
python django_forum/manage.py collectstatic --noinput

echo "All setup tasks completed!"

exec "$@"