from ..models import Cluster, User
from resources import ProtectedResource
from . import api
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .fields import cluster_fields as fields
from .fields import get_cluster_fields as get_fields
from flask_jwt import current_user
from onelove import OneLove


parser = api.parser()
parser.add_argument('name', type=str, required=True, location='json')


@ns_cluster.route('', endpoint='api/cluster')
class ClusterListAPI(ProtectedResource):
    @api.marshal_with(get_fields)
    def get(self):
        return [cluster for cluster in Cluster.objects.all()]

    @api.doc(body=fields)
    @api.marshal_with(fields)
    def post(self):
        args = parser.parse_args()
        cluster_name = args.get('name')
        cluster = Cluster(cluster_name)
        user = User.objects.get(id=current_user.get_id())
        cluster_role = OneLove.user_datastore.find_or_create_role(
            name=cluster_name,
            description="Cluster %s" % cluster_name
        )
        OneLove.user_datastore.add_role_to_user(user, cluster_role)
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
        args = parser.parse_args()
        cluster.name = args.get('name')
        cluster.save()
        return cluster

    @api.marshal_with(fields)
    def delete(self, id):
        cluster = self._find_cluster(id)
        cluster.delete()
        return cluster
