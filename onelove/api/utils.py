import os

from ..models.provision import Provision
from ..tasks.provision import playbook


def call_provision(workflow=None, task=None):
    args = []
    my_dir = os.path.dirname(__file__)
    project_root = os.path.abspath('{}/../..'.format(my_dir))
    playbook_file = '{}/playbook.yml'.format(project_root)
    inventory_file = '{}/inventory'.format(project_root)
    provision = Provision()
    provision.save()
    playbook.delay(
        provision.id,
        '-i',
        inventory_file,
        '-c',
        'local',
        playbook_file,
        *args,
    )
    provision.save()
    return {'status': 'OK'}
