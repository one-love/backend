import os
import sys
from json import dumps

import click
from celery.bin import worker as w
from flask.cli import AppGroup

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
        """
        List format:
            {
                "_meta": {
                    "hostvars": {
                        "oneloveback": {
                            "ansible_connection": "jail",
                            "ansible_python_interpreter": "/usr/bin/env python3.6",
                        }
                    }
                },
                "all": {
                    "children": [
                        "ungrouped"
                    ]
                },
                "ungrouped": {
                    "hosts": [
                        "oneloveback"
                    ]
                }
            }

        Host format:
            {
                "ansible_connection": "jail",
                "ansible_python_interpreter": "/usr/bin/env python3.6"
            }
        """
        if [list_hosts, host] == [False, None]:
            sys.stderr.write(
                'At least one option should be passed: --list or --host\n'
            )
            exit(1)
        provision_id = os.environ.get('PROVISION_ID', None)
        if provision_id is None:
            sys.stderr.write('PROVISION_ID env var must be set\n')
            exit(1)

        python_version = os.environ.get('PY_VERSION', '3.6')
        python_interpreter = '/usr/bin/env python{}'.format(python_version)
        if list_hosts:
            from ..models.provider import Provider
            hosts = []
            for provider in Provider.objects():
                hosts.extend(provider.hosts)
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
                    'ansible_host': host.ip,
                    'ansible_python_interpreter': python_interpreter,
                }
        else:
            data = {
                'ansible_host': '127.0.0.1',
                'ansible_python_interpreter': python_interpreter,
            }
        print(dumps(data, indent=4))

    app.cli.add_command(ansible)
    app.cli.add_command(celery)
