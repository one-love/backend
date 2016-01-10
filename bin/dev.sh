#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
while true; do
    ${PROJECT_ROOT}/manage.py runserver
    sleep 3
done
