from flask_restplus import abort
from resources import ProtectedResource

from .fields.task import fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster


@ns_cluster.route(
    '/<cluster_id>/services/<service_id>/provision',
    endpoint='cluster.service.provision',
)
class ClusterServiceProvisionAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, service_id):
        from ..tasks.provision import provision
        cluster = self._find_cluster(cluster_id)
        for service in cluster.services:
            if str(service.id) == service_id:
                return provision.delay(cluster_id, service_id)
        abort(404, 'Service %s not found' % service_id)
