from .. import current_app


@current_app.socketio.on('cluster', namespace='/onelove')
def cluster_message(message):
    print(message)


messages = [
    cluster_message
]
