#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG="dev"

find "${PROJECT_ROOT}" -name '*.pyc' -delete
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"

python "${PROJECT_ROOT}/worker.py"
