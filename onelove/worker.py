import time
import zmq
from onelove.utils import eprint


def worker(queue):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')
    while True:
        task_id = socket.recv()
        queue.put(task_id)
        socket.send('ok')
        time.sleep(0.1)
