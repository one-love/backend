import threading
from json import loads

from redis import StrictRedis


class SocketThread(threading.Thread):
    def __init__(self, socketio, redis_host, daemon=True):
        threading.Thread.__init__(self, daemon=daemon)
        self.socketio = socketio
        self.redis = StrictRedis(host=redis_host)
        self.listener = self.redis.pubsub()
        self.listener.subscribe('ansible')

    def run(self):
        message_type = 'ansible'
        for message in self.listener.listen():
            if message['type'] == 'message':
                data = loads(message['data'])
                self.socketio.emit(
                    message_type,
                    data,
                    namespace='/pulsar',
                )
