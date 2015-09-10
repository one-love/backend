from . import api

ns_auth = api.namespace('auth', description='Auth operations')
ns_cluster = api.namespace('clusters', description='Clusters operations')
ns_user = api.namespace('users', description='Users operations')
ns_task = api.namespace('tasks', description='Tasks operations')
