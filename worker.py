#!/usr/bin/env python
from mongoengine import connect
from traceback import print_exc
from multiprocessing import Process, Queue

from onelove.tasks import provision
from onelove.models import Task
from onelove.providers.ssh import ProviderSSH
from onelove.worker import worker
from onelove.utils import eprint


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
