#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

if [ "$(whoami)" = "devel" ]; then
    if [ ! -d ~/.virtualenvs/imaginevr ]; then
        vex --make imaginevr pip install -U pip
    fi
    . ~/.virtualenvs/imaginevr/bin/activate
fi

cd "${PROJECT_ROOT}"
pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
${PROJECT_ROOT}/load_data.py
