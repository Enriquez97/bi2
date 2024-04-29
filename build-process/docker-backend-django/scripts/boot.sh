#!/bin/bash
set -e

echo "nisira-bi:boot:env:${APP_ENVIRONMENT}"

python manage.py makemigrations

python manage.py migrate
python manage.py collectstatic --noinput

if [ "$APP_ENVIRONMENT" == "Local" ]; then
  echo "nisira-bi:run:local" && python manage.py runserver 0.0.0.0:8080 --insecure
fi
