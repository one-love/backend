import os
from ansible.plugins.callback import CallbackBase

context = zmq.Context()

class CallbackModule(CallbackBase):
    def log(self, result, status):
        task_id = os.getenv('TASK_ID')
        with open('/usr/src/app/provision.txt', 'w+') as log_file:
            log_file.write('task [%s], status [%s]' % (task_id, status))
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://backend:5500')
        socket.send_json({'task': task_id, 'status': status})
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
