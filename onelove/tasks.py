from celery import current_app
from models import Task


@current_app.task
def add(x, y):
    return x + y


@current_app.task(bind=True)
def provision(self, cluster, app):
    task = Task()
    task.celery_id = self.request.id
    task.save()
    return {
        'id': str(task.id),
        'celery_id': str(task.celery_id),
    }
