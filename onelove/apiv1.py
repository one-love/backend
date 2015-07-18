from flask.ext.restful import Resource, reqparse, fields, marshal_with

from models import Server
from provisioner import add


server_fields = {
    'name': fields.String,
    'description': fields.String,
    'live': fields.Boolean,
}


class ServerListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            type=str,
            required=True,
            help='No server name provided',
            location='json'
        )
        self.reqparse.add_argument(
            'description',
            type=str,
            default="",
            location='json'
        )
        super(ServerListAPI, self).__init__()

    @marshal_with(server_fields)
    def get(self):
        return [server for server in Server.objects.all()]
