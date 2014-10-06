One Love REST API
=================

[![Build Status](https://travis-ci.org/one-love/api.svg?branch=master)](https://travis-ci.org/one-love/api)
[![Coverage Status](https://coveralls.io/repos/one-love/api/badge.png?branch=master)](https://coveralls.io/r/one-love/api?branch=master)

This is Django based API part of [One Love](https://one-love.github.io/) project.

### Requirements and development setup
- VirtualBox
  - All boxes are tested in VirtualBox virtualization platform
- Vagrant
  - To run all VirtualBox instances effortlessly, Vagrant is used to automate VM creation/provisioning/destruction
- Ansible
  - Server setup and configuration is done through Ansible for One Love, as for all other applications

### First run
Clone this repo, `cd` into it, and run `vagrant up`. The process will take a while and should give you fully configured VirtualBox VM instance. Execute `vagrant ssh onelove` and you'll be inside VM, ready to develop. Run `~/bin/runserver.sh` and point your browser to [Vagrant VM](http://192.168.33.33:8000)

### Contributing to One Love
We will happily accept pull requests that conform to our [Contributing guidelines](CONTRIBUTING.md)
