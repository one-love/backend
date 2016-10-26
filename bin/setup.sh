#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

if [ -x /usr/local/bin/cbsd ]; then
    cbsd jstart mongodb
fi
find "${PROJECT_ROOT}" -name '*.pyc' -delete
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
cp "${PROJECT_ROOT}/local_config.dev.py" "${PROJECT_ROOT}/local_config.py"
