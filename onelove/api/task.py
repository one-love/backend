from flask_restplus import abort

from ..models import Task
from .fields.task import fields
from .namespaces import ns_task
from .resources import ProtectedResource


@ns_task.route('', endpoint='tasks')
class TaskListAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self):
        """Get list of tasks"""
        return [task for task in Task.objects.all()]


@ns_task.route('/<id>', endpoint='task')
class TaskAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self, id):
        """Find task by id"""
        try:
            task = Task.objects.get(id=id)
        except:
            abort(404, 'No such task')
        return task
