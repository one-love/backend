FROM python:2-slim

MAINTAINER Tilda Center <office@tilda.center>
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN mkdir -p ~/.ssh
COPY ssh_config ~/.ssh/config

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential \
    ca-certificates \
    libffi-dev \
    libssl-dev \
    libyaml-dev \
    openssh-client \
    python-dev \
    sshpass \
    tar \
    unzip \
    wget && \
    wget https://releases.hashicorp.com/consul-template/0.14.0/consul-template_0.14.0_linux_amd64.zip -O consul-template.zip && \
    unzip consul-template.zip && \
    mv consul-template /usr/bin && \
    rm -rf consul-template* && \
    wget -q -O - https://bootstrap.pypa.io/get-pip.py | python2 && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential python-dev wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app


CMD ["bin/start.sh"]
EXPOSE 9000
