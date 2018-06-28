import zmq

from flask_restplus import abort
from flask_jwt import current_identity

from .fields.provision import fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .resources import ProtectedResource
from ..models import Cluster, Service, Provision, User


@ns_cluster.route(
    '/<cluster_id>/services/<service_id>/provision',
    endpoint='cluster_service_provision',
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

        user_id = str(current_identity['id'])
        user = User.objects.get(id=user_id)
        provision = Provision(
            cluster=cluster,
            service=service,
            user=user,
        )
        provision.save()

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://worker:5555')
        socket.send(str(provision.pk))
        socket.recv()

        socket.close()
        context.term()
        return provision
