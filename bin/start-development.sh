#!/bin/bash

export C_FORCE_ROOT=yes
consul-template -once -config /usr/src/app/consul/onelove.conf
celery -A manage.celery worker --workdir /usr/src/app --loglevel INFO --pidfile /run/celery.pid --autoreload &
sleep 2
export FLASK_CONFIG=dev
python manage.py runserver
