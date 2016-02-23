FROM debian:jessie

MAINTAINER Zoran Olujić <olujicz@gmail.com>
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_common.txt /usr/src/app/

RUN mkdir -p ~/.ssh
COPY ssh_config ~/.ssh/config

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential \
    wget \
    sshpass \
    tar \
    python-dev \
    ca-certificates \
    libyaml-dev && \
    wget https://github.com/hashicorp/consul-template/releases/download/v0.10.0/consul-template_0.10.0_linux_amd64.tar.gz -O consul-template.tar.gz && \
    tar -xf consul-template.tar.gz && \
    mv consul-template_*/consul-template /usr/bin && \
    rm -rf consul-template* && \
    wget -q -O - https://bootstrap.pypa.io/get-pip.py | python2 && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential python-dev wget && \
    rm -rf /var/lib/apt/lists/*



CMD ["bin/start.sh"]
EXPOSE 5000 5555 9000
