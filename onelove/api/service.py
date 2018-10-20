from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_restplus import abort
from mongoengine.queryset import NotUniqueError

from ..models.auth import User
from ..models.service import Service
from .mixins import ServiceMixin
from .namespaces import ns_service
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ServiceSchema


@ns_service.route('', endpoint='services')
class ServiceListAPI(ProtectedResource):
    @ns_service.expect(parser)
    def get(self):
        """List services"""
        return paginate(Service.objects(), ServiceSchema())

    @ns_service.response(409, 'Service with that name already exists')
    @ns_service.expect(ServiceSchema.fields())
    def post(self):
        """Create service"""
        email = get_jwt_identity()
        user = User.objects.get(email=email)
        schema = ServiceSchema()
        service, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        service.user = user.pk
        try:
            service.save()
        except NotUniqueError:
            abort(409, error='Service with that name already exists')
        response, errors = schema.dump(service)
        if errors:
            return errors, 409
        return response


@ns_service.route('/<id>', endpoint='services_service')
@ns_service.response(404, 'Service not found')
class ServiceAPI(ProtectedResource, ServiceMixin):
    def get(self, id):
        """Show service details"""
        service = self.find_service(id)
        schema = ServiceSchema()
        response, errors = schema.dump(service)
        if errors:
            return errors, 409
        return response

    @ns_service.expect(ServiceSchema.fields())
    def patch(self, id):
        """Update service"""
        service = self.find_service(id)
        schema = ServiceSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        service.name = data.name or service.name
        service.save()
        response, errors = schema.dump(service)
        if errors:
            return errors, 409
        return response

    def delete(self, id):
        """Delete the service."""
        service = self.find_service(id)
        schema = ServiceSchema()
        response, errors = schema.dump(service)
        if errors:
            return errors, 409
        service.delete()
        return response
