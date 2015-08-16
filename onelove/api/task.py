from flask.ext.restful import fields, marshal_with

from resources import ProtectedResource
from ..models import Task


fields = {
    'id': fields.String,
    'celery_id': fields.String,
}


class TaskListAPI(ProtectedResource):
    @marshal_with(fields)
    def get(self):
        return [task for task in Task.objects.all()]


class TaskAPI(ProtectedResource):
    @marshal_with(fields)
    def get(self, id):
        from .. import current_app
        task = current_app.celery.AsyncResult(id=id)
        return task
