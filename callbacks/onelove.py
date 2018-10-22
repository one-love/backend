import inspect
import os
import sys
from datetime import datetime
from json import dumps, loads

from ansible.plugins.callback import CallbackBase

from mongoengine import connect
from redis import StrictRedis

DOCUMENTATION = '''
    name: onelove
    plugin_type: notification
    version_added: ""
    short_description: onelove
    description:
      - Callback to publish logs to redis
'''


def set_relative_path():
    frame = inspect.currentframe()
    file = inspect.getfile(frame)
    data = os.path.split(file)
    relpath = data[0]
    abspath = os.path.abspath(relpath)
    realpath = os.path.realpath('{}/..'.format(abspath))
    if realpath not in sys.path:
        sys.path.insert(0, realpath)


class CallbackModule(CallbackBase):
    def log(self, result, status):
        provision_id = os.environ.get('PROVISION_ID')
        data = {
            'host': result._host.get_name(),
            'provision_id': provision_id,
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
        mongodb_settings_string = os.environ.get('MONGODB_SETTINGS')
        if mongodb_settings_string is not None:
            set_relative_path()
            from onelove.models.provision import Provision, Log
            mongodb_settings = loads(mongodb_settings_string)
            connect(
                host=mongodb_settings['host'],
                db=mongodb_settings['db'],
            )
            provision = Provision.objects.get(id=provision_id)
            log = Log(
                host=data['host'],
                log=data['log'],
                status=data['status'],
                task=data['task'],
                timestamp=data['timestamp'],
            )
            provision.logs.append(log)
            provision.save()

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
