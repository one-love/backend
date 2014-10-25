FROM debian:stable
MAINTAINER Goran Mekić <meka@lugons.org>

ADD . /app
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yqq update && \
    apt-get -yqq upgrade && \
    apt-get install -yqq \
        libpq5 \
        libpython2.7 \
        postgresql-server-dev-9.1 \
        python \
        python-dev \
        python-pip && \
    sed 's:shippable:prod:g' /app/project/settings/__init__.py.template > /app/project/settings/__init__.py && \
    pip install -r /app/requirements.txt && \
    apt-get purge -yqq \
        postgresql-server-dev-9.1 \
        python-dev \
        python-pip && \
    apt-get autoremove -yqq --purge && \
    apt-get clean -yqq

CMD /app/run.sh

VOLUME /static /media
EXPOSE 9000
