#!/bin/bash

COMMAND=${1:-/usr/src/app/bin/start-development.sh}

sudo systemctl stop onelove
sudo docker run -it --rm -p 5000:5000 -p 5555:5555 -p 9000:9000 -v /vagrant/projects/backend:/usr/src/app --link mongodb:mongodb --link rabbitmq:rabbitmq onelove/backend:latest $COMMAND
sudo systemctl start onelove
