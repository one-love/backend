from celery.result import AsyncResult

from ..models import Task
from .fields.task import fields
from .namespaces import ns_task
from .resources import ProtectedResource


@ns_task.route('', endpoint='tasks')
class TaskListAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self):
    	"""Get list of tasks"""
        from .. import current_app
        current_app.socketio.emit('response', 'flask', namespace='/onelove')
        return [task for task in Task.objects.all()]


@ns_task.route('/<id>', endpoint='task')
class TaskAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self, celery_id):
    	"""Find task by the celery ID"""
        task = Task.objects.get(celery_id=celery_id)
    def get(self, id):
        task = AsyncResult(id)
        return task
