import zmq.green as zmq


def monitor():
    from . import current_app
    from .models import Task

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5500')
    while True:
        task_json = socket.recv_json()
        task = Task.objects.get(pk=task_json['id'])
        current_app.socketio.emit(
            'task',
            {
                'id': task['id'],
                'status': task.status,
            },
            namespace='/onelove',
            room=str(task.user.pk),
        )
        socket.send_json({'status': 'ok'})
    socket.close()
    context.tern()
