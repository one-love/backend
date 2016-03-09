from ..models import Service
from resources import ProtectedResource
from .mixins import ClusterMixin, ServiceMixin
from .namespaces import ns_service
from .namespaces import ns_cluster
from .fields import service_fields as fields
from .fields import get_service_fields as get_fields
import pagination


parser = ns_service.parser()
parser.add_argument('name', type=str, required=True, location='json')


@ns_service.route('', endpoint='services')
class ServiceListAPI(ProtectedResource):
    @ns_service.marshal_with(get_fields)
    @ns_service.doc(parser=pagination.parser)
    def get(self):
        """List services"""
        args = pagination.parser.parse_args()
        page = args.get('page')
        per_page = args.get('per_page')

        services = Service.objects().paginate(page, per_page)
        paging = pagination.Pagination(services)

        return services.items, 200, paging.headers

    @ns_service.doc(body=fields)
    @ns_service.marshal_with(get_fields)
    def post(self):
        """Create service"""
        args = parser.parse_args()
        service_name = args.get('name')
        service = Service(service_name)
        service.save()
        return service, 201


@ns_service.route('/<id>', endpoint='services.service')
class ServiceAPI(ProtectedResource, ServiceMixin):
    @ns_service.marshal_with(get_fields)
    @ns_service.response(404, 'Cluster not found')
    def get(self, id):
        """Show service details"""
        service = self._find_service(id)
        return service

    @ns_service.expect(fields)
    @ns_service.marshal_with(fields)
    def put(self, id):
        """Update service"""
        service = self._find_service(id)
        args = parser.parse_args()
        service.name = args.get('name')
        service.save()
        return service

    @ns_service.marshal_with(fields)
    def delete(self, id):
        """Delete the service."""
        service = self._find_service(id)
        service.delete()
        return service


@ns_cluster.route('/<cluster_id>/services', endpoint='clusters.services')
class ClusterServiceListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        return cluster.services
