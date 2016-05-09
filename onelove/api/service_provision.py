import zmq

from flask_restplus import abort
from resources import ProtectedResource

from .fields.task import fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from ..models import Cluster, Service, Task


@ns_cluster.route(
    '/<cluster_id>/services/<service_id>/provision',
    endpoint='cluster.service.provision',
)
class ClusterServiceProvisionAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    @ns_cluster.response(404, 'Service not found')
    def get(self, cluster_id, service_id):
        """Run provision"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except:
            abort(404, 'No such cluster')

        try:
            service = Service.objects.get(id=service_id)
        except:
            abort(404, 'No such service')
        task = Task(cluster=cluster, service=service)
        task.save()

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://worker:5555')
        socket.send(str(task.pk))
        socket.recv()

        socket.close()
        context.term()
        return task
