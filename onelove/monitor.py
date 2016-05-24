import zmq.green as zmq


def monitor():
    from . import current_app
    from .models import Task

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5500')
    while True:
        task_json = socket.recv_json()
        socket.send_json({'status': 'ok'})
        task = Task.objects.get(pk=task_json['id'])
        data = {}
        message_type = task_json['type']
        if task_json['type'] == 'task':
            data = {
                'id': task_json['id'],
                'status': task.status,
            }
        elif task_json['type'] == 'log':
            data = {
                'id': task_json['id'],
                'status': task_json['status'],
                'log': task_json['log'],
            }
        else:
            continue
        current_app.socketio.emit(
            message_type,
            data,
            namespace='/onelove',
            room=str(task.user.pk),
        )
    socket.close()
    context.tern()
