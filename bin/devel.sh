#!/bin/sh

export FLASK_ENV=development
export FLASK_PORT=${FLASK_PORT:=5000}
export PY=${PY:="python3.6"}
RUNNING_HOST=""
if [ -e "/.dockerenv" ]; then
	RUNNING_HOST="localhost"
else
	RUNNING_HOST=`hostname`
fi
API_PATH="api/v0/doc/"
API_ROOT="http://${RUNNING_HOST}:${FLASK_PORT}/${API_PATH}"
BIN_DIR=`dirname $0`
PROJECT_ROOT=`readlink -f "${BIN_DIR}/.."`
VIRTUALENV=${VIRTUALENV:="backend"}

if [ ! -d ~/.virtualenvs/${VIRTUALENV} ]; then
    ${PY} -m venv ~/.virtualenvs/${VIRTUALENV}
fi
. ~/.virtualenvs/${VIRTUALENV}/bin/activate

cd ${PROJECT_ROOT}
pip install -U -r requirements_dev.txt
echo "Backend"
echo "==============="
echo " * API_ROOT: ${API_ROOT}"
flask run -h 0.0.0.0 -p ${FLASK_PORT}
