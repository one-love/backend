import zmq.green as zmq


def monitor():
    from . import current_app
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5500')
    while True:
        task = socket.recv_json()
        current_app.socketio.emit(
            'task',
            {
                'id': task['id'],
                'status': task['status'],
            },
            namespace='/onelove',
            room=task['room'],
        )
        socket.send_json({'status': 'ok'})
    socket.close()
    context.tern()
