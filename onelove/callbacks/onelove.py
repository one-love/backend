from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    def v2_runner_on_ok(self, result):
        from celery import current_task
        data = {
            'host': result._host.get_name(),
            'task': result._task.get_name(),
        }
        current_task.send_event('ansible-log', **data)
