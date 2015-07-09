#!/bin/bash
docker run -it --rm --name flask-development -p 5000:5000 -v /vagrant/projects/api:/usr/src/app flask-docker
