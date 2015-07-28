from flask.ext.restful import Resource, reqparse, fields, marshal_with

from ..models import Application


fields = {
    'application_name': fields.String,
    'galaxy_role': fields.String,
    'id': fields.String,
    'name': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')


class ApplicationListAPI(Resource):
    @marshal_with(fields)
    def get(self):
        return [application for application in Application.objects.all()]

    @marshal_with(fields)
    def post(self):
        args = reqparse.parse_args()
        application = Application(
            name=args.get('name'),
        )
        application.save()
        return application


class ApplicationAPI(Resource):
    @marshal_with(fields)
    def get(self, id):
        try:
            application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            return {'message': 'Application does not exist'}
        return application

    @marshal_with(fields)
    def put(self, id):
        args = reqparse.parse_args()
        application = Application.objects.get(id=id)
        application.name = args.get('name')
        application.save()
        return application

    def delete(self, id):
        try:
            application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            return {'message': 'Application does not exist'}
        application.delete()
        return {'message': 'deleted'}
