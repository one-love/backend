from flask_rest_api import Blueprint, abort

from ..models.cluster import Cluster
from ..schemas.cluster import ClusterSchema
from ..schemas.paging import PagingSchema
from .methodviews import ProtectedMethodView

cluster = Blueprint('cluster', 'cluster')


@cluster.route('/', endpoint='clusters')
class ClusterListAPI(ProtectedMethodView):
    @cluster.arguments(PagingSchema(), location='headers')
    @cluster.response(ClusterSchema(many=True))
    def get(self, pagination):
        """List clusters"""
        return Cluster.objects.all()

    @cluster.arguments(ClusterSchema())
    @cluster.response(ClusterSchema())
    def post(self, args):
        """Create cluster"""
        cluster = Cluster(**args)
        cluster.save()
        return cluster


@cluster.route('/<cluster_id>', endpoint='cluster')
class ClusterAPI(ProtectedMethodView):
    @cluster.response(ClusterSchema())
    def get(self, cluster_id):
        """Get cluster details"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            return {'message': 'Cluster not found'}, 404
        return cluster

    @cluster.arguments(ClusterSchema(partial=True))
    @cluster.response(ClusterSchema())
    def patch(self, args, cluster_id):
        """Edit cluster details"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            return {'message': 'Cluster not found'}, 404
        cluster.name = args.get('name', cluster.name)
        cluster.save()
        return cluster

    @cluster.response(ClusterSchema())
    def delete(self, cluster_id):
        """Delete cluster"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort('Cluster not found', 404)
        cluster.delete()
        return cluster
