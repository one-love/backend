from resources import ProtectedResource
from ..models import Task
from .namespaces import ns_task
from .fields.task import fields


@ns_task.route('', endpoint='tasks')
class TaskListAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self):
    	"""Get list of tasks"""
        return [task for task in Task.objects.all()]


@ns_task.route('/<celery_id>', endpoint='task')
class TaskAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self, celery_id):
    	"""Find task by the celery ID"""
        task = Task.objects.get(celery_id=celery_id)
        return task
