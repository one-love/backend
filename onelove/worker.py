import os
import zmq
from shutil import copyfile
from multiprocessing import Process

from onelove.plugin import load_hosting_providers
from onelove.tasks.provision import provision
from plugins import HOSTING_PROVIDERS


context = zmq.Context()
load_hosting_providers(HOSTING_PROVIDERS)


def setup_ssh(project_root):
    home = os.getenv('HOME', '')
    ssh_dir = '%s/.ssh' % home
    ssh_config = '%s/config' % ssh_dir
    ssh_config_template = '%s/templates/ssh-config' % project_root
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)
    copyfile(ssh_config_template, ssh_config)


def run(project_root, config):
    setup_ssh(project_root)
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')

    while True:
        task_id = socket.recv()
        worker = Process(target=provision, args=(task_id, config))
        worker.start()
        socket.send(task_id)
