from flask import current_app
from flask_restplus import abort

from ..models.cluster import Cluster
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ClusterSchema


@ns_cluster.route('', endpoint='clusters')
class ClusterListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.expect(parser)
    def get(self):
        """Get list of a clusters"""
        return paginate(Cluster.objects(), ClusterSchema())

    @ns_cluster.expect(ClusterSchema.fields())
    def post(self):
        """Create aplication for the service"""
        schema = ClusterSchema()
        cluster, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        cluster.save()
        response, errors = schema.dump(cluster)
        if errors:
            return errors, 409
        return response


@ns_cluster.route('/<cluster_id>', endpoint='cluster')
class ClusterAPI(ProtectedResource):
    def get(self, cluster_id):
        """Get cluster details"""
        try:
            cluster = Cluster.objects().get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, 'No such cluster')
        schema = ClusterSchema()
        response, errors = schema.dump(cluster)
        if errors:
            return errors, 409
        return response

    @ns_cluster.expect(ClusterSchema.fields(required=False))
    def patch(self, cluster_id):
        """Change cluster details"""
        try:
            cluster = Cluster.objects().get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, 'No such cluster')
        schema = ClusterSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        cluster.name = data.name or cluster.name
        response, errors = schema.dump(cluster)
        if errors:
            return errors, 409
        cluster.save()
        return response

    def delete(self, cluster_id):
        """Delete the cluster"""
        try:
            cluster = Cluster.objects().get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, 'No such cluster')
        schema = ClusterSchema()
        response, errors = schema.dump(cluster)
        if errors:
            return errors, 409
        cluster.delete()
        return response
