FROM debian:jessie
MAINTAINER Goran Mekić <meka@lugons.org>

ENV DEBIAN_FRONTEND noninteractive

ADD . /app
ADD bin /bin
RUN /bin/build.sh

CMD /bin/run.sh

VOLUME /static /media
EXPOSE 9000
