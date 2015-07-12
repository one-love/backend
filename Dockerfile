FROM python:2-onbuild
MAINTAINER Zoran Olujić <olujicz@gmail.com>

CMD ["uwsgi", "-s", "0.0.0.0:9000", "-w", "manage:manager.app"]
EXPOSE 5000 9000
