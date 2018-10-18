import os
from datetime import datetime
from json import dumps

from ansible.plugins.callback import CallbackBase

from redis import StrictRedis

DOCUMENTATION = '''
    name: onelove
    plugin_type: notification
    version_added: ""
    short_description: onelove
    description:
      - Callback to publish logs to redis
'''


class CallbackModule(CallbackBase):
    def log(self, result, status):
        data = {
            'host': result._host.get_name(),
            'provision_id': os.environ.get('PROVISION_ID'),
            'log': result._result.get('msg'),
            'status': status,
            'task': result._task.get_name(),
            'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S:%f'),
            'type': 'log',
        }
        redis_host = os.environ.get('REDIS_HOST')
        redis = StrictRedis(host=redis_host)
        message = dumps(data)
        redis.publish('ansible', message)

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
