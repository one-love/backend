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
load_hosting_providers(HOSTING_PROVIDERS)


def worker(queue):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')
    while True:
        task_id = socket.recv()
        queue.put(task_id)
        socket.send('ok')
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
