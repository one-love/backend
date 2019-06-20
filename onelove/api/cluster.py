from flask_rest_api import Blueprint, abort

from ..models.cluster import Cluster
from ..schemas.cluster import ClusterSchema
from ..schemas.paging import PagingSchema
from .methodviews import ProtectedMethodView

blueprint = Blueprint('cluster', 'cluster')


@blueprint.route('/', endpoint='clusters')
class ClusterListAPI(ProtectedMethodView):
    @blueprint.arguments(PagingSchema(), location='headers')
    @blueprint.response(ClusterSchema(many=True))
    def get(self, pagination):
        """List clusters"""
        return Cluster.objects.all()

    @blueprint.arguments(ClusterSchema())
    @blueprint.response(ClusterSchema())
    def post(self, args):
        """Create cluster"""
        cluster = Cluster(**args)
        cluster.save()
        return cluster


@blueprint.route('/<cluster_id>', endpoint='cluster')
class ClusterAPI(ProtectedMethodView):
    @blueprint.response(ClusterSchema())
    def get(self, cluster_id):
        """Get cluster details"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            return {'message': 'Cluster not found'}, 404
        return cluster

    @blueprint.arguments(ClusterSchema(partial=True))
    @blueprint.response(ClusterSchema())
    def patch(self, args, cluster_id):
        """Edit cluster details"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            return {'message': 'Cluster not found'}, 404
        cluster.name = args.get('name', cluster.name)
        cluster.save()
        return cluster

    @blueprint.response(ClusterSchema())
    def delete(self, cluster_id):
        """Delete cluster"""
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort('Cluster not found', 404)
        cluster.delete()
        return cluster
