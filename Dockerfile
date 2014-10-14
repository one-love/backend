FROM python:2-onbuild
MAINTAINER Goran Mekić <meka@lugons.org>
RUN ["cp", "project/settings/__init__.py.template", "project/settings/__init__.py"]
EXPOSE 8000
