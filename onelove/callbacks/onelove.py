import os
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    def v2_runner_on_ok(self, result):
        data = {
            'host': result._host.get_name(),
            'task': result._task.get_name(),
        }
        task_id = os.getenv('TASK_ID')
        with open('/usr/src/app/provision.txt', 'w+') as log_file:
            log_file.write('task id: %s' % task_id)
        return data
