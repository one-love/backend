import os
import subprocess
from datetime import datetime
from json import dumps

from celery.utils.log import get_task_logger
from flask import current_app
from redis import StrictRedis

from ..models.provision import Provision
from .celery import celery

logger = get_task_logger(__name__)

datetime_format = '%Y-%m-%dT%H:%M:%S:%f'


@celery.task(bind=True)
def playbook(self, provision_id, *args):
    os.environ['PROVISION_ID'] = str(provision_id)
    os.environ['REDIS_HOST'] = current_app.config['REDIS_HOST']
    playbook_args = list(args)
    playbook_args.insert(0, 'ansible-playbook')
    playbook_args.append('--ssh-common-args')
    playbook_args.append(
        '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    )
    provision = Provision.objects.get(id=provision_id)
    provision.status = 'RUNNING'
    provision.save()
    redis_host = current_app.config['REDIS_HOST']
    redis = StrictRedis(host=redis_host)
    data = {
        'provision_id': provision_id,
        'status': provision.status,
        'type': 'log',
        'timestamp': datetime.utcnow().strftime(datetime_format),
    }
    redis.publish('ansible', dumps(data))
    result = subprocess.run(playbook_args)
    if result.returncode != 0:
        provision.status = 'FAILURE'
        provision.save()
        data['status'] = provision.status
        redis.publish('ansible', dumps(data))
        return provision.status
    provision.status = 'SUCCESS'
    provision.save()
    data['status'] = provision.status
    redis.publish('ansible', dumps(data))
    return provision.status
