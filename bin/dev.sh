#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG="dev"

find "${PROJECT_ROOT}" -name '*.pyc' -delete
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
cp "${PROJECT_ROOT}/local_config.dev.py" "${PROJECT_ROOT}/local_config.py"

while true; do
    sleep 5
    ${PROJECT_ROOT}/backend.py runserver
done
