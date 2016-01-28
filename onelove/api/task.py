from resources import ProtectedResource
from ..models import Task
from . import api
from .namespaces import ns_task
from .fields import task_fields as fields


@ns_task.route('', endpoint='tasks')
class TaskListAPI(ProtectedResource):
    @api.marshal_with(fields)
    def get(self):
        return [task for task in Task.objects.all()]


@ns_task.route('/<id>', endpoint='task')
class TaskAPI(ProtectedResource):
    @api.marshal_with(fields)
    def get(self, id):
        from .. import current_app
        task = current_app.celery.AsyncResult(id=id)
        return task
