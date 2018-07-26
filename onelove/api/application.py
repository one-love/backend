from flask_restplus import abort
from .resources import ProtectedResource

from .fields.application import fields
from .mixins import ServiceMixin
from .namespaces import ns_service

from ..models import Application, Service
from ..utils import check_fields, all_fields_optional


parser = ns_service.parser()
parser.add_argument('galaxy_role', type=str, required=True, location='json')
parser.add_argument('name', type=str, required=True, location='json')


@ns_service.route(
    '/<service_id>/applications',
    endpoint='services_applications'
)
class ServiceApplicationListAPI(ProtectedResource, ServiceMixin):
    @ns_service.marshal_with(fields)
    def get(self, service_id):
        """Get list of a aplications for the service"""
        service = self._find_service(service_id)
        return service.applications

    @ns_service.expect(fields)
    @ns_service.marshal_with(fields)
    def post(self, service_id):
        """Create aplication for the service"""
        service = self._find_service(service_id)
        args = parser.parse_args()
        check_fields(args)
        galaxy_role = args.get('galaxy_role')
        name = args.get('name')
        for app in service.applications:
            if app.name == name:
                abort(409, error='Application with that name already exists')
        app = Application(
            galaxy_role=galaxy_role,
            name=name,
        )
        service.applications.append(app)
        service.save()
        return app


@ns_service.route(
    '/<service_id>/applications/<application_name>',
    endpoint='services_application'
)
@ns_service.response(404, 'No such application')
class ServiceApplicationAPI(ProtectedResource, ServiceMixin):
    @ns_service.marshal_with(fields)
    def get(self, service_id, application_name):
        """Get application for the service"""
        service = self._find_service(service_id)
        for app in service.applications:
            if app.name == application_name:
                return app
        abort(404, error='No such application')

    @ns_service.expect(fields)
    @ns_service.marshal_with(fields)
    @ns_service.expect(fields)
    @ns_service.marshal_with(fields)
    def patch(self, service_id, application_name):
        """Update application for the service"""
        patch_parser = all_fields_optional(parser)
        args = patch_parser.parse_args()
        service = Service.objects.get(id=service_id)
        for app in service.applications:
            if app.name == application_name:
                app.name = args.get('name') or app.name
                app.galaxy_role = args.get('galaxy_role') or app.galaxy_role
                service.save()
                return app
        abort(404, error='No such application')

    @ns_service.marshal_with(fields)
    def delete(self, service_id, application_name):
        """Delete appliaction in the service"""
        service = self._find_service(service_id)
        for app in service.applications:
            if app.name == application_name:
                service.applications.remove(app)
                service.save()
                return app
        abort(404, error='No such application')
