#!/bin/bash

export C_FORCE_ROOT=yes
celery -A manage.celery worker --workdir=/usr/src/app &
uwsgi -s 0.0.0.0:9000 -w manage:app
