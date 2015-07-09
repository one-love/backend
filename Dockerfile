FROM python:2-onbuild
MAINTAINER Zoran Olujić <olujicz@gmail.com>

CMD [ "python", "./manage.py", "runserver" ]
EXPOSE 5000
