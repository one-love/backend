#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
${PROJECT_ROOT}/load_data.py
