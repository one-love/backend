#!/bin/bash

function kill_system_service()
{
    echo -n 'Stopping system api service ... '
    sudo systemctl stop api
    echo 'done'

    echo -n 'Kill api docker, if exists ... '
    docker kill api &>/dev/null
    echo 'done'

    echo -n 'Remove api docker, if exists ... '
    docker rm api &>/dev/null
    echo 'done'
}


function start_development_mode()
{
    echo 'Starting development mode'
    export DOCKER_CONTAINER_ID=$(docker run -dtiP --name api --dns 172.17.42.1 -v /vagrant/projects/api:/app --volumes-from consul-template onelove/api --python-autoreload 1)

    sleep 10
    echo -n 'Restart nginx ... '
    sudo systemctl restart nginx
    echo 'done'

    docker attach $DOCKER_CONTAINER_ID
}


function stop_development_mode()
{
    echo 'Stopping docker container'
    docker stop $DOCKER_CONTAINER_ID
    docker kill $DOCKER_CONTAINER_ID
    docker rm $DOCKER_CONTAINER_ID

    echo -n 'Starting system api service ... '
    sudo systemctl start api
    echo 'done'

    echo -n 'Restart nginx ... '
    sudo systemctl restart nginx
    echo 'done'
}

kill_system_service
start_development_mode
stop_development_mode
