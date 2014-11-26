FROM debian:jessie
MAINTAINER Goran Mekić <meka@lugons.org>

ENV DEBIAN_FRONTEND noninteractive

ADD . /app
RUN /app/bin/build.sh

CMD /app/bin/run.sh

VOLUME /static /media
EXPOSE 9000
