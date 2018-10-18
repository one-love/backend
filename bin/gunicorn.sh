#!/bin/sh


BIN_DIR=`dirname $0`
FLASK_ENV="production"
NAME=onelove
NUM_WORKERS=4
WSGI_MODULE=wsgi
PORT=${PORT:=9000}
LOG_LEVEL=info
WORKER_CLASS=eventlet

. ${BIN_DIR}/common.sh
setup


exec gunicorn ${WSGI_MODULE}:app \
  --name ${NAME} \
  --workers ${NUM_WORKERS} \
  --worker-class ${WORKER_CLASS} \
  --bind=:${PORT} \
  --log-level=${LOG_LEVEL} \
  --log-file=- \
  --capture-output
