from flask import current_app
from flask_restplus import abort

from .mixins import ServiceMixin
from .namespaces import ns_service
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ApplicationSchema


@ns_service.route(
    '/<service_id>/applications',
    endpoint='service_applications'
)
class ApplicationListAPI(ProtectedResource, ServiceMixin):
    @ns_service.expect(parser)
    def get(self, service_id):
        """Get list of a aplications for the service"""
        service = self.find_service(service_id)
        return paginate(service.applications, ApplicationSchema())

    @ns_service.expect(ApplicationSchema.fields())
    def post(self, service_id):
        """Create aplication for the service"""
        service = self.find_service(service_id)
        schema = ApplicationSchema()
        app, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        for service_app in service.applications:
            if app.name == service_app.name:
                abort(409, error='Application with that name already exists')
        response = schema.dump(app)
        service.applications.append(app)
        service.save()
        return response


@ns_service.route(
    '/<service_id>/applications/<application_name>',
    endpoint='service_application'
)
@ns_service.response(404, 'No such application')
class ApplicationAPI(ProtectedResource, ServiceMixin):
    def get(self, service_id, application_name):
        """Get application for the service"""
        service = self.find_service(service_id)
        schema = ApplicationSchema()
        for app in service.applications:
            if app.name == application_name:
                response, errors = schema.dump(app)
                if errors:
                    return errors, 409
                return response
        abort(404, error='No such application')

    @ns_service.expect(ApplicationSchema.fields())
    def patch(self, service_id, application_name):
        """Update application for the service"""
        schema = ApplicationSchema(partial=True)
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        service = self.find_service(service_id)
        for app in service.applications:
            if app.name == application_name:
                app.name = data.name or app.name
                app.galaxy_role = data.galaxy_role or app.galaxy_role
                service.save()
                return schema.dump(app)
        abort(404, error='No such application')

    def delete(self, service_id, application_name):
        """Delete appliaction in the service"""
        service = self.find_service(service_id)
        schema = ApplicationSchema()
        for app in service.applications:
            if app.name == application_name:
                service.applications.remove(app)
                response, errors = schema.dump(app)
                if errors:
                    return errors, 409
                service.save()
                return response
        abort(404, error='No such application')
