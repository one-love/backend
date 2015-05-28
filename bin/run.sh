#!/bin/bash

/app/bin/restart.sh $@

while true; do
    consul-template -config /app/consul/api.conf
    $COMMAND
    sleep 1
done
