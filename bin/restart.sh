#!/bin/bash

uwsgi --stop /run/uwsgi.pid
python /app/manage.py migrate --noinput
python /app/manage.py loaddata initial
python /app/manage.py collectstatic --noinput
uwsgi --ini /app/uwsgi.ini $@
