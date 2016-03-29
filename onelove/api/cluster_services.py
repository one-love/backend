from flask_restplus import abort
from onelove.api.fields import (
    service_fields as fields,
    post_cluster_service_fields as post_fields,
    task_fields,
)
from onelove.api.mixins import ClusterMixin
from onelove.api.namespaces import ns_cluster
from onelove.models import Service, User
from onelove.api.resources import ProtectedResource


parser = ns_cluster.parser()
parser.add_argument('service', type=str, required=True, location='json')
parser.add_argument('email', type=str, required=True, location='json')


@ns_cluster.route(
    '/<cluster_id>/services',
    endpoint='clusters.cluster.services',
)
class ClusterServiceListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        return cluster.services

    @ns_cluster.doc(body=post_fields)
    @ns_cluster.marshal_with(fields)
    def post(self, cluster_id):
        args = parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        service_name = args.get('service')
        service_user_email = args.get('email')
        for service in cluster.services:
            if service.name == service_name:
                abort(
                    409,
                    'Service %s is already part of cluster %s' % (
                        service.name,
                        cluster.name,
                    )
                )

        try:
            user = User.objects.get(email=service_user_email)
        except User.DoesNotExist:
            abort(404, 'No such user')

        try:
            service = Service.objects.get(name=service_name, user=user)
        except Service.DoesNotExist:
            abort(404, 'No such service')

        cluster.services.append(service)
        cluster.save()
        return service


@ns_cluster.route(
    '/<cluster_id>/services/<user>/<service_name>',
    endpoint='clusters.cluster.service',
)
class ClusterServiceAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def delete(self, cluster_id, user, service_name):
        cluster = self._find_cluster(cluster_id)
        for service in cluster.services:
            if service.name == service_name and user == service.user.email:
                cluster.services.remove(service)
                cluster.save()
                return service
        abort(
            404,
            'Service %s with user %s not found' % (
                service_name,
                user,
            )
        )
        return service


@ns_cluster.route(
    '/<cluster_id>/services/<user>/<service_name>/provision',
    endpoint='clusters.cluster.service.provision',
)
class ClusterServiceProvisionAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(task_fields)
    def get(self, cluster_id, user, service_name):
        cluster = self._find_cluster(cluster_id)
        task = {
            'id': '123',
            'celery_id': '456',
        }
        for service in cluster.services:
            if service.name == service_name and user == service.user.email:
                return task
        abort(
            404,
            'Service %s with user %s not found' % (
                service_name,
                user,
            )
        )
