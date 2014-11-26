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

# Upgrade all packages and install needed ones
apt-get -y update
apt-get -y upgrade
apt-get install -y ${INSTALL_PACKAGES}

# Install Python packages
pip install -r /app/requirements.txt

# Cleanup to save space
apt-get purge -y ${REMOVE_PACKAGES}
apt-get autoremove -y --purge
apt-get clean -y
