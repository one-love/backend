from ..models import Cluster, User
from resources import ProtectedResource
from . import api
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .fields import cluster_fields as fields
from .fields import get_cluster_fields as get_fields
from flask_jwt import current_identity
from .. import current_app


parser = api.parser()
parser.add_argument('name', type=str, required=True, location='json')


@ns_cluster.route('', endpoint='api/cluster')
class ClusterListAPI(ProtectedResource):
    @api.marshal_with(get_fields)
    def get(self):
        """List clusters"""
        clusters = []
        for cluster in Cluster.objects(roles__in=current_identity.roles):
            clusters.append(cluster)
        return clusters

    @api.doc(body=fields)
    @api.marshal_with(get_fields)
    def post(self):
        """Create cluster"""
        args = parser.parse_args()
        cluster_name = args.get('name')
        cluster = Cluster(cluster_name)

        admin_role = current_app.user_datastore.find_or_create_role(
            name='admin_' + cluster_name,
            description="Cluster %s admin" % cluster_name,
            admin=True,
        )
        cluster.roles.append(admin_role)

        user_role = current_app.user_datastore.find_or_create_role(
            name='user_' + cluster_name,
            description="Cluster %s users" % cluster_name,
            admin=False,
        )
        cluster.roles.append(user_role)
        cluster.save()

        user = User.objects.get(id=current_identity.get_id())

        current_app.user_datastore.add_role_to_user(user, admin_role)
        return cluster, 201


@ns_cluster.route('/<id>', endpoint='cluster/cluster')
class ClusterAPI(ProtectedResource, ClusterMixin):
    @api.marshal_with(get_fields)
    def get(self, id):
        """Show cluster details"""
        cluster = self._find_cluster(id)
        return cluster

    @api.expect(fields)
    @api.marshal_with(fields)
    def put(self, id):
        """Update cluster"""
        cluster = self._find_cluster(id)
        args = parser.parse_args()
        cluster.name = args.get('name')
        cluster.save()
        return cluster

    @api.marshal_with(fields)
    def delete(self, id):
        """Delete the cluster."""
        cluster = self._find_cluster(id)
        cluster.delete()
        return cluster
