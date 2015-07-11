from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask_restful_swagger import swagger

from models import Server


api = swagger.docs(Api(), apiVersion='0.1')

server_fields = {
    'name': fields.String,
    'description': fields.String,
    'live': fields.Boolean,
    'uri': fields.Url('server')
}


class ServerListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No server name provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(ServerListAPI, self).__init__()

    def get(self):
        return {'servers': [{'name': server.name, 'description': server.description, 'live': server.live} for server in Server.objects.all()]}

    def post(self):
        args = self.reqparse.parse_args()
        server = {
            'id': servers[-1]['id'] + 1,
            'name': args['name'],
            'description': args['description'],
            'live': False
        }
        servers.append(server)
        return {'server': marshal(server, server_fields)}, 201


class ServerAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('live', type=bool, location='json')
        super(ServerAPI, self).__init__()

    def get(self, id):
        server = [server for server in servers if server['id'] == id]
        if len(server) == 0:
            abort(404)
        return {'server': marshal(server[0], server_fields)}

    def put(self, id):
        server = [server for server in servers if server['id'] == id]
        if len(server) == 0:
            abort(404)
        server = server[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                server[k] = v
        return {'server': marshal(server, server_fields)}

    def delete(self, id):
        server = [server for server in servers if server['id'] == id]
        if len(server) == 0:
            abort(404)
        servers.remove(server[0])
        return {'result': True}


api.add_resource(ServerListAPI, '/api/v1.0/servers', endpoint='servers')
api.add_resource(ServerAPI, '/api/v1.0/servers/<int:id>', endpoint='server')
