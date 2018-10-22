import os
from json import dumps

from flask import current_app
from flask_restplus import abort

from ..tasks.provision import playbook
from .schemas import ProvisionOptionsSchema


def call_provision(provision_id):
    args = []
    my_dir = os.path.dirname(__file__)
    project_root = os.path.abspath('{}/../..'.format(my_dir))
    playbook_file = '{}/playbook.yml'.format(project_root)
    inventory_file = '{}/inventory'.format(project_root)
    schema = ProvisionOptionsSchema()
    data, errors = schema.load(current_app.api.payload)
    if errors:
        abort(409, errors)
    playbook.delay(
        provision_id,
        '-i',
        inventory_file,
        '-c',
        'local',
        playbook_file,
        *args,
    )
    return {'status': 'OK'}
