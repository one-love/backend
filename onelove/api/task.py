from flask.ext.restful import fields, marshal_with

from resources import ProtectedResource


fields = {
    'id': fields.String,
    'status': fields.String,
}


class TaskAPI(ProtectedResource):
    @marshal_with(fields)
    def get(self, id):
        from .. import current_app
        task = current_app.celery.AsyncResult(id=id)
        return task
