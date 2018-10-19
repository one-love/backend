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
