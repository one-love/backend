#!/bin/sh

BIN_DIR=`dirname $0`
export FLASK_ENV="development"
. ${BIN_DIR}/common.sh
setup no
flask $@
