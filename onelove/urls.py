from api.cluster import (
    ClusterListAPI,
    ClusterAPI,
    ClusterApplicationListAPI,
    ClusterApplicationAPI,
    ClusterApplicationProvisionAPI,
    ClusterProviderListAPI,
    ClusterProviderAPI,
)
from api.task import TaskListAPI, TaskAPI
from api.user import UserListAPI, UserAPI
from api.auth import AuthAPI


def init(api):
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
        ClusterProviderListAPI,
        '/clusters/<cluster_id>/providers',
        endpoint='api/cluster/providers'
    )
    api.add_resource(
        ClusterProviderAPI,
        '/clusters/<cluster_id>/providers/<provider_name>',
        endpoint='api/cluster/provider'
    )
    api.add_resource(
        TaskListAPI,
        '/tasks',
        endpoint='api/tasks'
    )
    api.add_resource(
        TaskAPI,
        '/tasks/<id>',
        endpoint='api/task'
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
    api.add_resource(
        AuthAPI,
        '/auth',
        endpoint='api/auth'
    )
