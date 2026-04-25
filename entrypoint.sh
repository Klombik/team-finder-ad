#!/bin/sh
set -e

until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

python manage.py migrate
# python manage.py seed_demo
exec "$@"
