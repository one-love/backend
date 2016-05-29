from . import api

ns_auth = api.namespace('auth', description='Auth operations')
ns_cluster = api.namespace('clusters', description='Clusters operations')
ns_me = api.namespace('me', description='Me operations')
ns_plugin = api.namespace('plugins', description='Plugin operations')
ns_service = api.namespace('services', description='Service operations')
ns_provision = api.namespace('provisions', description='Provision operations')
ns_user = api.namespace('users', description='Users operations')
