import json
import time
import zmq
from threading import Thread

from . import current_app


thread = None


def monitor():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')
    while True:
        task = json.loads(socket.recv())
        current_app.socketio.emit(
            'task',
            {
                'id': task['id'],
                'status': task['status'],
            }
        )
        socket.send('ok')
        time.sleep(0.1)


def setup_monitor():
    global thread
    if thread is None:
        thread = Thread(target=monitor)
        thread.daemon = True
        thread.start()
