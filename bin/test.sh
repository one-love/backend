#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

find "${PROJECT_ROOT}" -name '*.pyc' -delete
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
cd "${PROJECT_ROOT}"
nosetests
