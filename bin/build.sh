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

# Get consul-template
wget https://github.com/hashicorp/consul-template/releases/download/v0.9.0/consul-template_0.9.0_linux_amd64.tar.gz -O /tmp/consul-template.tar.gz
cd /tmp
tar xfvp consul-template.tar.gz
cp **/consul-template /usr/bin
rm -rf consul-template*

# Cleanup to save space
apt-get purge -y ${REMOVE_PACKAGES}
apt-get autoremove -y --purge
apt-get clean -y
