from apiv1 import ServerListAPI


def init(api):
    api.add_resource(ServerListAPI, '/api/v1.0/servers', endpoint='servers')
