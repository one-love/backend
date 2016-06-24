#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

"${PROJECT_ROOT}/bin/install_gcc.sh"
find "${PROJECT_ROOT}" -name '*.pyc' -delete
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"

sleep 5
${PROJECT_ROOT}/load_data.py
