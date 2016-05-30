import os
import zmq.green as zmq
from ansible.plugins.callback import CallbackBase
from datetime import datetime


context = zmq.Context()


class CallbackModule(CallbackBase):
    def log(self, result, status):
        task_id = os.getenv('PROVISION_ID')
        data = {
            'id': task_id,
            'status': status,
            'type': 'log',
            'log': result._result.get('msg'),
            'host': result._host.get_name(),
            'task': result._task.get_name(),
            'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S:%f'),
        }
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://backend:5500')
        socket.send_json(data)
        socket.recv_json()
        socket.close()

    def v2_playbook_on_handler_task_start(self, result):
        self.log(result, 'start')

    def v2_runner_on_ok(self, result):
        self.log(result, 'ok')

    def v2_runner_on_unreachable(self, result):
        self.log(result, 'unreachable')

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.log(result, 'failed')

    def v2_runner_on_skipped(self, result):
        self.log(result, 'skipped')

    def v2_runner_item_on_ok(self, result):
        self.log(result, 'item_ok')

    def v2_runner_item_on_skipped(self, result):
        self.log(result, 'item_skipped')

    def v2_runner_item_on_failed(self, result):
        self.log(result, 'item_failed')
