FROM python:2-onbuild
MAINTAINER Zoran Olujić <olujicz@gmail.com>

RUN wget https://github.com/hashicorp/consul-template/releases/download/v0.10.0/consul-template_0.10.0_linux_amd64.tar.gz -O consul-template.tar.gz && \
    tar xf consul-template.tar.gz && \
    mv consul-template_*/consul-template /usr/bin && \
    rm -rf consul-template*
CMD ["bin/start.sh"]
EXPOSE 5000 5555 9000
