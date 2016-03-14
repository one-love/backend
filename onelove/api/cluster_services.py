import flask_restplus
from onelove.api.fields import service_fields as fields, post_service_fields as post_fields
from onelove.api.mixins import ClusterMixin
from onelove.api.namespaces import ns_cluster
from onelove.models import Service
from onelove.api.resources import ProtectedResource


parser = ns_cluster.parser()
parser.add_argument('service', type=str, required=True, location='json')


@ns_cluster.route('/<cluster_id>/services', endpoint='clusters.services')
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
        for service in cluster.services:
            if service.name == service_name:
                flask_restplus.abort(409, 'Service %s is already part of cluster %s' % (service.name, cluster.name))

        service = Service.objects.get(name=service_name)
        cluster.services.append(service)
        cluster.save()
        return service
