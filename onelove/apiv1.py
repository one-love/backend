from flask.ext.restful import Resource, reqparse, fields

from models import Server
from provisioner import add


server_fields = {
    'name': fields.String,
    'description': fields.String,
    'live': fields.Boolean,
    'result': fields.Integer,
    'uri': fields.Url('server')
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

    def get(self):
        result = add.delay(2, 5)
        return {'servers': [
            {
                'name': server.name,
                'description': server.description,
                'live': server.live,
                'result': result.get(timeout=1),
            }
            for server in Server.objects.all()
        ]}
