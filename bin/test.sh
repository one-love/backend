#!/bin/sh


set -e


export FLASK_ENV="testing"
BIN_DIR=`dirname $0`
. ${BIN_DIR}/common.sh
setup


CI=${1}
if [ "${CI}" = "ci" ]; then
  cp local_config_ci.py local_config.py
fi


pip install -U -r requirements_dev.txt
rm -rf `find . -name __pycache__`
rm -rf .pytest_cache
py.test --cov=onelove --cov-report=xml
