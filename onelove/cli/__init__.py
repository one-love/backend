import os
import sys
from json import dumps

import click
from celery.bin import worker as w
from flask.cli import AppGroup
from flask_security.cli import users
from onelove.models.auth import User

ansible = AppGroup('ansible', short_help='Ansible operations')
celery = AppGroup('celery', short_help='Manage celery worker')


def register(app):
    @celery.command()
    def start():
        worker = w.worker(app=app.celery)
        worker.run(
            loglevel=app.config['CELERY_LOG_LEVEL'],
            traceback=True,
            pool_cls='eventlet',
        )

    @ansible.command()
    @click.option('--list', 'list_hosts', help='List hosts', is_flag=True)
    @click.option('--host', help='Details about specified host')
    def hosts(list_hosts, host):
        """Return ansible hosts"""
        if [list_hosts, host] == [False, None]:
            sys.stderr.write(
                'At least one option should be passed: --list or --host\n'
            )
            exit(1)
        provision_id = os.environ.get('PROVISION_ID', None)
        if provision_id is None:
            sys.stderr.write('PROVISION_ID env var must be set\n')
            exit(1)

        from ..models.provision import Provision
        try:
            provision = Provision.objects.get(id=provision_id)
        except Provision.DoesNotExist:
            sys.stderr.write('No such provision\n')
            exit(1)
        hosts = []
        for provider in provision.cluster.providers:
            hosts.extend(provider.list())
        python_version = os.environ.get('PY_VERSION', '3.6')
        python_interpreter = '/usr/bin/env python{}'.format(python_version)
        if list_hosts:
            data = {
                '_meta': {
                    'hostvars': {},
                },
                'all': {
                    'children': [
                        'ungrouped',
                    ],
                },
                'ungrouped': {
                    'hosts': [host.hostname for host in hosts],
                },
            }
            for host in hosts:
                data['_meta']['hostvars'][host.hostname] = {
                    'ansible_python_interpreter': python_interpreter,
                }
                if host.ip:
                    device_data = data['_meta']['hostvars'][host.hostname]
                    device_data['ansible_host'] = host.ip
            print(dumps(data, indent=4))
        else:
            for host in hosts:
                if host.hostname == host:
                    data = {
                        'ansible_python_interpreter': python_interpreter,
                    }
                    if host.ip:
                        data['ansible_host'] = host.ip
                    print(dumps(data, indent=4))
                    return
            sys.stderr.write('No such host\n')
            exit(1)

    @users.command()
    @click.argument('email')
    def admin(email):
        """Proclaim user an admin"""
        try:
            user = User.objects.get(email=email)
            user.admin = True
            user.save()
        except User.DoesNotExist:
            print('No such user')

    @users.command()
    @click.argument('email')
    def deadmin(email):
        """Remove admin priviledges from user"""
        try:
            user = User.objects.get(email=email)
            user.admin = False
            user.save()
        except User.DoesNotExist:
            print('No such user')

    app.cli.add_command(ansible)
    app.cli.add_command(celery)
