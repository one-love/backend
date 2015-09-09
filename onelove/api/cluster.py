from flask.ext.restplus import reqparse

from ..models import Cluster
from resources import ProtectedResource
from . import api
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .fields import cluster_fields as fields
from .fields import get_cluster_fields as get_fields


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')


@ns_cluster.route('', endpoint='api/cluster')
class ClusterListAPI(ProtectedResource):
    @api.marshal_with(get_fields)
    def get(self):
        return [cluster for cluster in Cluster.objects.all()]

    @api.expect(fields)
    @api.marshal_with(fields)
    def post(self):
        args = reqparse.parse_args()
        cluster = Cluster(
            name=args.get('name'),
        )
        cluster.save()
        return cluster, 201


@ns_cluster.route('/<id>', endpoint='cluster/cluster')
class ClusterAPI(ProtectedResource, ClusterMixin):
    @api.marshal_with(get_fields)
    def get(self, id):
        cluster = self._find_cluster(id)
        return cluster

    @api.expect(fields)
    @api.marshal_with(fields)
    def put(self, id):
        cluster = self._find_cluster(id)
        args = reqparse.parse_args()
        cluster.name = args.get('name')
        cluster.save()
        return cluster

    @api.marshal_with(fields)
    def delete(self, id):
        cluster = self._find_cluster(id)
        cluster.delete()
        return cluster
