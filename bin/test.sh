#!/bin/sh


set -e


BIN_DIR=`dirname $0`
export FLASK_ENV="testing"
. ${BIN_DIR}/common.sh
setup


CI=${1}
if [ "${CI}" = "ci" ]; then
  cp local_config_ci.py local_config.py
fi
rm -rf `find . -name __pycache__`
rm -rf .pytest_cache
flake8 .
py.test --cov=onelove --cov-report=xml
