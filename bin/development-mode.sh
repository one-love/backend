#!/bin/bash

docker run -it --rm -p 5000:5000 -v /vagrant/projects/api:/usr/src/app flask-docker
