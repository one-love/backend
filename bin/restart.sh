#!/bin/bash

export C_FORCE_ROOT=yes

if [ -s /run/celery.pid ]; then
    CELERY_PID=$(cat /run/celery.pid)
    kill -SIGHUP $CELERY_PID
else
    celery -A manage.celery worker --logfile /var/log/celery.log --detach --workdir /usr/src/app --loglevel INFO --pidfile /run/celery.pid
    celery -A manage.celery worker --workdir /usr/src/app --loglevel INFO --pidfile /run/celery.pid --autoreload &
fi

if [ -s /run/uwsgi.pid ]; then
    touch /usr/src/app/uwsgi.ini
else
    uwsgi --ini /usr/src/app/uwsgi.ini
fi
