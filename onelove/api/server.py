from flask.ext.restful import Resource, reqparse, fields, marshal_with

from ..models import Server


server_fields = {
    'name': fields.String,
    'description': fields.String,
    'live': fields.Boolean,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')
reqparse.add_argument('description', type=str, default="", location='json')
reqparse.add_argument('live', type=bool, default=False, location='json')


class ServerListAPI(Resource):
    @marshal_with(server_fields)
    def get(self):
        return [server for server in Server.objects.all()]

    @marshal_with(server_fields)
    def post(self):
        args = reqparse.parse_args()
        server = Server(
            name=args.get('name'),
            description=args.get('description'),
            live=args.get('live'),
        )
        server.save()
        return server


class ServerAPI(Resource):
    @marshal_with(server_fields)
    def get(self, id):
        try:
            server = Server.objects.get(id=id)
        except Server.DoesNotExist:
            return {'message': 'Server does not exist'}
        return server

    @marshal_with(server_fields)
    def put(self, id):
        args = reqparse.parse_args()
        server = Server.objects.get(id=id)
        server.name = args.get('name')
        server.description = args.get('description')
        server.live = args.get('live')
        server.save()
        return server

    def delete(self, id):
        try:
            server = Server.objects.get(id=id)
        except Server.DoesNotExist:
            return {'message': 'Server does not exist'}
        server.delete()
        return {'message': 'deleted'}
