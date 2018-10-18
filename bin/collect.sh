#!/bin/sh


BIN_DIR=`dirname $0`
. ${BIN_DIR}/common.sh
setup

rm -rf onelove/static
flask collect --verbose
rm -rf onelove/static/app
