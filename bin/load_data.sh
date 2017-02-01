#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

if [ "$(whoami)" = "devel" ]; then
    if [ ! -d ~/.virtualenvs/one-love ]; then
        vex --make one-love pip install -U pip
    fi
    . ~/.virtualenvs/one-love/bin/activate
fi

cd "${PROJECT_ROOT}"
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
${PROJECT_ROOT}/load_data.py
