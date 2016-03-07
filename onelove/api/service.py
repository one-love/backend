from ..models import Service, User
from resources import ProtectedResource
from .mixins import ClusterMixin
from .namespaces import ns_service
from .fields import service_fields as fields
from .fields import get_service_fields as get_fields
from flask_jwt import current_identity
from flask import current_app
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

        services = Service.objects(
        ).paginate(page, per_page)
        paging = pagination.Pagination(services)

        return services.items, 200, paging.headers

    @ns_service.doc(body=fields)
    @ns_service.marshal_with(get_fields)
    def post(self):
        """Create service"""
        args = parser.parse_args()
        service_name = args.get('name')
        service = Service(service_name)

        admin_role = current_app.onelove.user_datastore.find_or_create_role(
            name='admin_' + service_name,
            description="Service %s admin" % service_name,
            admin=True,
        )

        user_role = current_app.onelove.user_datastore.find_or_create_role(
            name='user_' + service_name,
            description="Service %s users" % service_name,
            admin=False,
        )
        service.save()

        user = User.objects.get(id=current_identity.get_id())

        current_app.onelove.user_datastore.add_role_to_user(user, admin_role)
        return service, 201
