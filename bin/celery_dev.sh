#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG='dev'
cd ${PROJECT_ROOT}
celery -A manage_celery.celery worker --loglevel INFO -P solo
