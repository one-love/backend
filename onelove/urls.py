from api.application import ApplicationListAPI, ApplicationAPI
from api.cluster import (
    ClusterListAPI,
    ClusterAPI,
    ClusterApplicationListAPI,
    ClusterApplicationAPI,
    ClusterApplicationProvisionAPI,
)
from api.task import TaskAPI
from api.user import UserListAPI, UserAPI


def init(api):
    api.add_resource(
        ApplicationListAPI,
        '/applications',
        endpoint='api/applications'
    )
    api.add_resource(
        ApplicationAPI,
        '/applications/<id>',
        endpoint='api/application'
    )
    api.add_resource(
        ClusterListAPI,
        '/clusters',
        endpoint='api/clusters'
    )
    api.add_resource(
        ClusterAPI,
        '/clusters/<id>',
        endpoint='api/cluster'
    )
    api.add_resource(
        ClusterApplicationListAPI,
        '/clusters/<cluster_id>/applications',
        endpoint='api/cluster/applications'
    )
    api.add_resource(
        ClusterApplicationAPI,
        '/clusters/<cluster_id>/applications/<application_name>',
        endpoint='api/cluster/application'
    )
    api.add_resource(
        ClusterApplicationProvisionAPI,
        '/clusters/<cluster_id>/applications/<application_name>/provision',
        endpoint='api/cluster/application/provision'
    )
    api.add_resource(
        TaskAPI,
        '/tasks/<id>',
        endpoint='api/tasks'
    )
    api.add_resource(
        UserListAPI,
        '/users',
        endpoint='api/users'
    )
    api.add_resource(
        UserAPI,
        '/users/<id>',
        endpoint='api/user'
    )
