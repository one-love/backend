#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG="dev"

if [ -z "${TMUX}" ]; then
    "${PROJECT_ROOT}/setup.sh"
fi

while true; do
    echo "One Love Backend"
    echo "==============="
    ${PROJECT_ROOT}/backend.py runserver
    sleep 5
done
