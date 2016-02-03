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
    apt-get install -y build-essential wget sshpass tar python-dev python-pip && \
    wget https://github.com/hashicorp/consul-template/releases/download/v0.10.0/consul-template_0.10.0_linux_amd64.tar.gz -O consul-template.tar.gz && \
    tar -xf consul-template.tar.gz && \
    mv consul-template_*/consul-template /usr/bin && \
    rm -rf consul-template* && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential python-dev wget python-pip


CMD ["bin/start.sh"]
EXPOSE 5000 5555 9000
