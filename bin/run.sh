#!/bin/bash

export COMMAND="consul-template -config /app/consul/api.conf"

echo -n "Waiting for initial config "
until $COMMAND -once; do
    echo -n "."
    sleep 3
done
echo " done"

/app/bin/restat.sh $@

$COMMAND &
sleep 1
tail -f /var/log/uwsgi.log
