#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG='dev'
export C_FORCE_ROOT='yes'

pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
cp "${PROJECT_ROOT}/local_config.dev.py" "${PROJECT_ROOT}/local_config.py"

sleep 5
cd ${PROJECT_ROOT}
celery -A manage_celery.celery worker --loglevel INFO -P solo -E
