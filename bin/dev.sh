#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
cp "${PROJECT_ROOT}/local_config.dev.py" "${PROJECT_ROOT}/local_config.py"
sleep 5
${PROJECT_ROOT}/create_default_admin.py
${PROJECT_ROOT}/manage.py runserver
