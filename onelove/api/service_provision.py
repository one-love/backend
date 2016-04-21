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
    @ns_cluster.expect(fields)
    @ns_cluster.response(404,'Service not found')
    def get(self, cluster_id, service_id):
        """Check for task status"""
        from ..models import Task
        from ..tasks.provision import provision
        cluster = self._find_cluster(cluster_id)
        for service in cluster.services:
            if str(service.id) == service_id:
                return provision.delay(cluster_id, service_id)
        abort(404, 'Service %s not found' % service_id)
