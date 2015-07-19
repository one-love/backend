from api.server import ServerListAPI, ServerAPI


def init(api):
    api.add_resource(ServerListAPI, '/api/v1.0/servers', endpoint='servers')
    api.add_resource(ServerAPI, '/api/v1.0/servers/<id>', endpoint='server')
