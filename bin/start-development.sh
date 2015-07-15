#!/bin/bash

consul-template -once -config /usr/src/app/consul/onelove.conf
python manage.py runserver
