from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    def v2_runner_on_ok(self, result):
        data = {
            'host': result._host.get_name(),
            'task': result._task.get_name(),
        }
        return data
