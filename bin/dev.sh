#!/bin/sh

export FLASK_CONFIG="dev"
BIN_DIR=`dirname $0`
PROJECT_ROOT=`readlink -f "${BIN_DIR}/.."`

if [ -z "${TMUX}" ]; then
    "${PROJECT_ROOT}/bin/setup.sh"
fi

while true; do
    echo "One Love Backend"
    echo "==============="
    ${PROJECT_ROOT}/backend.py runserver
    sleep 5
done
