#!/bin/bash

set -e

export COMMAND="/opt/bin/consul-template -config /app/consul/api.conf"

echo -n "Waiting for initial config "
until $COMMAND -once; do
    echo -n "."
    sleep 3
done
echo " done"

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput
uwsgi --ini /app/uwsgi.ini $@

$COMMAND &
sleep 1
tail -f /var/log/uwsgi.log
