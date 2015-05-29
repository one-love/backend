#!/bin/bash

uwsgi --stop /run/uwsgi.pid
sleep 1
killall uwsgi
sleep 1
killall -9 uwsgi
python /app/manage.py migrate --noinput
python /app/manage.py loaddata initial
python /app/manage.py collectstatic --noinput
uwsgi --ini /app/uwsgi.ini $@
