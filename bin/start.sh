#!/bin/bash

touch /var/log/uwsgi.log /var/log/celery.log
tail -f /var/log/uwsgi.log /var/log/celery.log &

consul-template -config /usr/src/app/consul/onelove.conf
