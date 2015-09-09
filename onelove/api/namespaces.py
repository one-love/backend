from . import api

ns_auth = api.namespace('auth', description='Auth operations')
ns_cluster = api.namespace('cluster', description='Clusters operations')
ns_user = api.namespace('user', description='Users operations')
ns_task = api.namespace('task', description='Tasks operations')
