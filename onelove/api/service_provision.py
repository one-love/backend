import zmq

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
    @ns_cluster.response(404, 'Service not found')
    def get(self, cluster_id, service_id):
        """Run provision"""
        context = zmq.Context()
        print('Connecting to hello world server ...')
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://worker:5555')
        print('Sending request')
        socket.send(b'Hello')
        message = socket.recv()
        print('Received reply: %s' % message)
