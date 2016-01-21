from flask_restplus import abort
from .mixins import ClusterMixin
from resources import ProtectedResource
from ..models import HostSSH
from . import api
from .fields import host_fields as fields
from .namespaces import ns_cluster


parser = api.parser()
parser.add_argument('hostname', type=str, required=True, location='json')
parser.add_argument('ip', type=str, required=True, location='json')


@ns_cluster.route(
    '/<cluster_id>/providers/<provider_name>/hosts',
    endpoint='api/cluster/provider/hosts',
)
class ClusterProviderHostListAPI(ProtectedResource, ClusterMixin):
    @api.marshal_with(fields)
    def get(self, cluster_id, provider_name):
        cluster = self._find_cluster(cluster_id)
        provider = None
        for prov in cluster.providers:
            if prov.name == provider_name:
                provider = prov
                break
        if not provider:
            abort(404, 'No such provider')
        return provider.hosts

    @api.expect(fields)
    @api.marshal_with(fields)
    def post(self, cluster_id, provider_name):
        args = parser.parse_args()
        hostname = args.get('hostname')
        ip = args.get('ip')
        provider = self._find_provider(cluster_id, provider_name)
        host = HostSSH(hostname=hostname, ip=ip)
        provider.hosts.append(host)
        provider.save()
        cluster = self._find_cluster(cluster_id)
        cluster.save()
        return provider.hosts
