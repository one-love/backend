from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_restplus import abort
from mongoengine.queryset import NotUniqueError

from ..models.auth import User
from ..models.service import Service
from .mixins import ServiceMixin
from .namespaces import ns_service
from .resources import ProtectedResource
from .schemas import ServiceSchema


@ns_service.route('', endpoint='services')
class ServiceListAPI(ProtectedResource):
    def get(self):
        """List services"""
        services = Service.objects.all()

        schema = ServiceSchema(many=True)
        response, errors = schema.dump(services)

        if errors:
            abort(409, errors)

        return response, 200

    @ns_service.response(409, 'Service with that name already exists')
    @ns_service.expect(ServiceSchema.fields())
    def post(self):
        """Create service"""
        email = get_jwt_identity()
        user = User.objects.get(email=email)
        schema = ServiceSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        service = Service(name=data.name, user=user.pk)
        try:
            service.save()
        except NotUniqueError:
            abort(409, error='Service with that name already exists')
        response = schema.dump(service)

        return response, 201


@ns_service.route('/<id>', endpoint='services_service')
@ns_service.response(404, 'Service not found')
class ServiceAPI(ProtectedResource, ServiceMixin):
    @ns_service.marshal_with(ServiceSchema.fields())
    def get(self, id):
        """Show service details"""
        service = self._find_service(id)
        return service

    @ns_service.expect(ServiceSchema.fields())
    def patch(self, id):
        """Update service"""
        service = self._find_service(id)
        schema = ServiceSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        service.name = data.name or service.name
        service.save()

        response = schema.dump(service)

        return response

    @ns_service.marshal_with(ServiceSchema.fields())
    def delete(self, id):
        """Delete the service."""
        service = self._find_service(id)

        service.delete()

        return service
