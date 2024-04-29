#!/bin/bash
set -e

echo "nisira-bi:boot:env:${APP_ENVIRONMENT}"


if [ "$APP_ENVIRONMENT" == "Local" ]; then
  echo "nisira-bi:run:local"
fi

celery -A backend worker -l info
