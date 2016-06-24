#!/bin/bash

if [ -z $(which gcc) ]; then
    apt-get update
    apt-get install -y gcc
fi
