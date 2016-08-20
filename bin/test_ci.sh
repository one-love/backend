#!/bin/bash

export PROJECT_ROOT=$(readlink -f "$(dirname $0)/..")
export FLASK_CONFIG="testing"
cd "${PROJECT_ROOT}"
pwd
cp local_config.ci.py local_config.py
pep8 **/*.py
nosetests --with-coverage --cover-branches --cover-erase --cover-xml --cover-xml-file=coverage.xml --cover-package onelove --with-xunit --xunit-file=nosetests.xml
