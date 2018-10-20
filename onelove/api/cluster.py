from flask import current_app

from ..models.cluster import Cluster
from ..models.provision import Provision
from .mixins import ClusterMixin, ServiceMixin
from .namespaces import ns_cluster
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ClusterSchema, ProvisionOptionsSchema, ProvisionSchema
from .utils import call_provision


@ns_cluster.route('', endpoint='clusters')
class ClusterListAPI(ProtectedResource):
    @ns_cluster.expect(parser)
    def get(self):
        """Get list of a clusters"""
        return paginate(Cluster.objects(), ClusterSchema())

    @ns_cluster.expect(ClusterSchema.fields())
    def post(self):
        """Create cluster"""
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
class ClusterAPI(ProtectedResource, ClusterMixin):
    def get(self, cluster_id):
        """Get cluster details"""
        cluster = self.find_cluster(cluster_id)
        schema = ClusterSchema()
        response, errors = schema.dump(cluster)
        if errors:
            return errors, 409
        return response

    @ns_cluster.expect(ClusterSchema.fields(required=False))
    def patch(self, cluster_id):
        """Change cluster details"""
        cluster = self.find_cluster(cluster_id)
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
        cluster = self.find_cluster(cluster_id)
        schema = ClusterSchema()
        response, errors = schema.dump(cluster)
        if errors:
            return errors, 409
        cluster.delete()
        return response


@ns_cluster.route(
    '/<cluster_id>/provision/<service_id>',
    endpoint='cluster_provision',
)
class ClusterProvisionAPI(ProtectedResource, ClusterMixin, ServiceMixin):
    @ns_cluster.expect(ProvisionOptionsSchema.fields())
    def post(self, cluster_id, service_id):
        """Get cluster details"""
        cluster = self.find_cluster(cluster_id)
        service = self.find_service(service_id)
        provision = Provision(service=service.id, cluster=cluster.id)
        provision.save()
        schema = ProvisionSchema()
        response, errors = schema.dump(provision)
        if errors:
            return errors, 409
        call_provision(str(provision.id))
        return response
