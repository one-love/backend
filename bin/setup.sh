#!/bin/sh

BIN_DIR=`dirname $0`
PROJECT_ROOT=`readlink -f "${BIN_DIR}/.."`

find "${PROJECT_ROOT}" -name '*.pyc' -delete
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
cp "${PROJECT_ROOT}/local_config.dev.py" "${PROJECT_ROOT}/local_config.py"
