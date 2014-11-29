FROM debian:jessie
MAINTAINER Goran Mekić <meka@lugons.org>

ENV DEBIAN_FRONTEND noninteractive

ADD . /app
RUN /app/bin/build.sh

ENTRYPOINT ["/app/bin/run.sh"]

VOLUME /static /media
EXPOSE 8000 9000
