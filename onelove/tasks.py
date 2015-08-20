from celery import current_app
from models import Task
import ansible.playbook
from ansible import callbacks


@current_app.task(bind=True)
def provision(self, cluster, app):
    task = Task()
    task.celery_id = self.request.id
    task.save()
    inventory = ansible.inventory.Inventory('inventory')
    playbook = 'site.yml'
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats)

    pb = ansible.playbook.PlayBook(
        playbook=playbook,
        inventory=inventory,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        remote_user='vagrant',
        remote_pass='vagrant',
    )

    result = pb.run()
    return {
        'id': str(task.id),
        'celery_id': str(task.celery_id),
    }



