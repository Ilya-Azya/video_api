#!/bin/sh
echo "Waiting for PostgreSQL to be available..."


while ! nc -z "$DJANGO_DB_HOST" "$DJANGO_DB_PORT"; do
  sleep 0.5
done

echo "PostgreSQL is up - running migrations"

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
