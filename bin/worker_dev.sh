#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG="dev"

find "${PROJECT_ROOT}" -name '*.pyc' -delete
if [ -z "${TMUX}" ]; then
    pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
fi

while true; do
    echo "One Love Worker"
    echo "==============="
    python "${PROJECT_ROOT}/worker.py"
    sleep 5
done
