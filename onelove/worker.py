import os
import time
import zmq
from mongoengine import connect
from multiprocessing import Process, Queue
from shutil import copyfile
from traceback import print_exc

from onelove.models import Task
from onelove.plugin import load_hosting_providers
from onelove.tasks import provision
from onelove.utils import eprint
from plugins import HOSTING_PROVIDERS


queue = Queue()
context = zmq.Context()
load_hosting_providers(HOSTING_PROVIDERS)


def listener():
    frontend = context.socket(zmq.REP)
    frontend.bind('tcp://*:5555')
    poll = zmq.Poller()
    poll.register(frontend)
    while True:
        sockets = dict(poll.poll(1000))
        if frontend in sockets and sockets[frontend] == zmq.POLLIN:
            task_id = frontend.recv()
            queue.put(task_id)
            frontend.send('ok')
            time.sleep(0.1)


def setup_ssh(project_root):
    home = os.getenv('HOME', '')
    ssh_dir = '%s/.ssh' % home
    ssh_config = '%s/config' % ssh_dir
    ssh_config_template = '%s/templates/ssh-config' % project_root
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)
    copyfile(ssh_config_template, ssh_config)


def run(project_root):
    setup_ssh(project_root)
    worker_process = Process(target=listener)
    worker_process.start()
    connect('onelove', host='mongodb')
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
