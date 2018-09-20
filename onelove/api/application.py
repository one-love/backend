from flask import current_app, request
from flask_restplus import abort

from ..models.service import Application, Service
from .mixins import ServiceMixin
from .namespaces import ns_service
from .resources import ProtectedResource
from .schemas import ApplicationSchema


@ns_service.route(
    '/<service_id>/applications',
    endpoint='services_applications'
)
class ServiceApplicationListAPI(ProtectedResource, ServiceMixin):
    def get(self, service_id):
        """Get list of a aplications for the service"""
        service = self._find_service(service_id)

        schema = ApplicationSchema(many=True)
        response, errors = schema.dump(service.applications)

        if errors:
            abort(409, errors)

        return response

    @ns_service.expect(ApplicationSchema.fields())
    def post(self, service_id):
        """Create aplication for the service"""
        service = self._find_service(service_id)

        schema = ApplicationSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409

        galaxy_role = data.galaxy_role
        name = data.name
        for app in service.applications:
            if app.name == name:
                abort(409, error='Application with that name already exists')
        app = Application(
            galaxy_role=galaxy_role,
            name=name,
        )

        response = schema.dump(app)

        service.applications.append(app)
        service.save()
        return response


@ns_service.route(
    '/<service_id>/applications/<application_name>',
    endpoint='services_application'
)
@ns_service.response(404, 'No such application')
class ServiceApplicationAPI(ProtectedResource, ServiceMixin):
    @ns_service.marshal_with(ApplicationSchema.fields())
    def get(self, service_id, application_name):
        """Get application for the service"""
        service = self._find_service(service_id)
        for app in service.applications:
            if app.name == application_name:
                return app
        abort(404, error='No such application')

    @ns_service.expect(ApplicationSchema.fields())
    def patch(self, service_id, application_name):
        """Update application for the service"""
        schema = ApplicationSchema(partial=True)
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409

        service = Service.objects.get(id=service_id)
        for app in service.applications:
            if app.name == application_name:
                app.name = data.name or app.name
                app.galaxy_role = data.galaxy_role or app.galaxy_role
                service.save()
                return schema.dump(app)
        abort(404, error='No such application')

    def delete(self, service_id, application_name):
        """Delete appliaction in the service"""
        schema = ApplicationSchema()
        service = self._find_service(service_id)
        for app in service.applications:
            if app.name == application_name:
                service.applications.remove(app)
                service.save()
                return schema.dump(app)
        abort(404, error='No such application')
