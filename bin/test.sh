#!/bin/sh

export PROJECT_DIR=`dirname $0`
export PROJECT_ROOT=`readlink -f ${PROJECT_DIR}/..`
export NOSETESTS_BIN=`which nosetests`

find "${PROJECT_ROOT}" -name '*.pyc' -delete
if [ -z "${NOSETESTS_BIN}" ]; then
    pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
fi
cp "${PROJECT_ROOT}/local_config.dev.py" "${PROJECT_ROOT}/local_config.py"
cd "${PROJECT_ROOT}"
pep8 **/*.py
nosetests
