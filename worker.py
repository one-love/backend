#!/usr/bin/env python
import os
from mongoengine import connect
from traceback import print_exc
from multiprocessing import Process, Queue
from shutil import copyfile

from onelove.tasks import provision
from onelove.models import Task
from onelove.plugin import load_hosting_providers
from onelove.worker import worker
from onelove.utils import eprint
from plugins import HOSTING_PROVIDERS


load_hosting_providers(HOSTING_PROVIDERS)

home = os.getenv('HOME', '')
project_root = os.path.dirname(os.path.abspath(__file__))
ssh_dir = '%s/.ssh' % home
ssh_config = '%s/config' % ssh_dir
ssh_config_template = '%s/templates/ssh-config' % project_root
if not os.path.exists(ssh_dir):
    os.makedirs(ssh_dir)
copyfile(ssh_config_template, ssh_config)

with open(ssh_config, 'r') as ssh_config_file:
    lines = ssh_config_file.readlines()
    eprint(ssh_config)
    for line in lines:
        eprint(line)


queue = Queue()
worker_process = Process(target=worker, args=(queue,))
worker_process.start()
connect('onelove', host='db')


while True:
    task_id = queue.get()
    task = Task.objects.get(id=task_id)
    task.status = 'STARTED'
    task.save()
    try:
        provision(task)
    except:
        print_exc()
        eprint('Task %s failed' % task_id)
        task.status = 'FAILED'
        task.save()
