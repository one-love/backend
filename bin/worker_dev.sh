#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")

pip install -U -r "${PROJECT_ROOT}/requirements_dev.txt"
python "${PROJECT_ROOT}/hwserver.py"
