from flask_rest_api import Blueprint, abort

from ..models.service import Service
from ..schemas.paging import PagingSchema
from ..schemas.service import ServiceSchema
from .methodviews import ProtectedMethodView

blueprint = Blueprint('service', 'service')


@blueprint.route('/', endpoint='services')
class ServiceListAPI(ProtectedMethodView):
    @blueprint.arguments(PagingSchema(), location='headers')
    @blueprint.response(ServiceSchema(many=True))
    def get(self, pagination):
        """List services"""
        return Service.objects.all()

    @blueprint.arguments(ServiceSchema())
    @blueprint.response(ServiceSchema())
    def post(self, args):
        """Create service"""
        service = Service(**args)
        service.save()
        return service


@blueprint.route('/<service_id>', endpoint='service')
class ServiceAPI(ProtectedMethodView):
    @blueprint.response(ServiceSchema())
    def get(self, service_id):
        """Get service details"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return {'message': 'Service not found'}, 404
        return service

    @blueprint.arguments(ServiceSchema(partial=True))
    @blueprint.response(ServiceSchema())
    def patch(self, args, service_id):
        """Edit service details"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return {'message': 'Service not found'}, 404
        service.name = args.get('name', service.name)
        service.save()
        return service

    @blueprint.response(ServiceSchema())
    def delete(self, service_id):
        """Delete service"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort('Service not found', 404)
        service.delete()
        return service
