#!/bin/bash
set -e

echo "Waiting for MySQL..."
until python -c "
import pymysql
pymysql.connect(host='db', user='root', password='rootpass', port=3306)
" 2>/dev/null; do
  echo "MySQL not ready, retrying in 2s..."
  sleep 2
done
echo "MySQL is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
