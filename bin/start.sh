#!/bin/bash

export C_FORCE_ROOT=yes
celery -A manage.celery worker --logfile /dev/stdout --detach --workdir=/usr/src/app
uwsgi --ini /usr/src/app/uwsgi.ini
