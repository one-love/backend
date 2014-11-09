#!/bin/bash

set -e

INSTALL_PACKAGES="\
    libpython2.7 \
    postgresql-server-dev-all \
    python python-dev \
    wget \
    python-pip \
"

REMOVE_PACKAGES="\
    postgresql-server-dev-all \
    python-dev \
    wget \
    python-pip \
"

rm -r /app/bin
# Upgrade all packages and install needed ones
apt-get -yqq update
apt-get -yqq upgrade
apt-get install -yqq ${INSTALL_PACKAGES}

# Install Python packages
pip install -r /app/requirements.txt

# Cleanup to save space
apt-get purge -yqq ${REMOVE_PACKAGES}
apt-get autoremove -yqq --purge
apt-get clean -yqq
