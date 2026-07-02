#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

PORT=${PORT:-8000}

echo "Starting application with Gunicorn on port $PORT..."

exec gunicorn slotflow.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120