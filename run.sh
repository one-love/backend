#!/bin/bash

set -e

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput
uwsgi \
    --chdir=/app \
    --module=project.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=project.settings \
    --master \
    --pidfile=/tmp/project-master.pid \
    --socket=:9000 \
    --processes=5 \
    --uid=1000 --gid=2000 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum
