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
        from ..models import Task
        from ..tasks.provision import provision
        cluster = self._find_cluster(cluster_id)
        task = {'status': 'PENDING'}
        for service in cluster.services:
            if str(service.id) == service_id:
                celery_id = provision.delay(cluster_id, service_id)
                task['celery_id'] = str(celery_id)
                return task
        abort(404, 'Service %s not found' % service_id)
