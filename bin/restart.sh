#!/bin/bash

if [ -s /run/celery.pid ]; then
    CELERY_PID=$(cat /run/celery.pid)
    kill -SIGHUP $CELERY_PID
else
    export C_FORCE_ROOT=yes
    celery -A manage.celery worker --logfile /var/log/celery.log --detach --workdir=/usr/src/app --log-level=INFO --pidfile=/run/celery.pid
fi

if [ -s /run/uwsgi.pid ]; then
    touch /usr/src/app/uwsgi.ini
else
    uwsgi --ini /usr/src/app/uwsgi.ini
fi
