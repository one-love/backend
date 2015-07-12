#!/bin/bash

COMMAND=${1:-python manage.py runserver}

sudo docker run -it --rm -p 5000:5000 -v /vagrant/projects/api:/usr/src/app --link mongodb:mongodb --link rabbitmq:rabbitmq onelove/api:latest $COMMAND
