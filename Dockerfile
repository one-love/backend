FROM python:2-onbuild
MAINTAINER Zoran Olujić <olujicz@gmail.com>

CMD ["bin/start.sh"]
EXPOSE 5000 9000
