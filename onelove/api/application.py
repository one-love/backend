from flask_rest_api import Blueprint, abort

from ..schemas.application import ApplicationSchema
from ..schemas.paging import PagingSchema
from .methodviews import ProtectedMethodView
from .service import blueprint


@blueprint.route('/<service_id>/applications', endpoint='service_applications')
class ApplicationListAPI(ProtectedMethodView):
    @blueprint.arguments(PagingSchema(), location='headers')
    @blueprint.response(ApplicationSchema(many=True))
    def get(self, pagination, service_id):
        """List applications"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, error='No such service')
        return service.applications

    @blueprint.arguments(ApplicationSchema())
    @blueprint.response(ApplicationSchema())
    def post(self, args):
        """Create application"""
        application = Application(**args)
        application.save()
        return application


@blueprint.route('/<application_id>', endpoint='application')
class ApplicationAPI(ProtectedMethodView):
    @blueprint.response(ApplicationSchema())
    def get(self, application_id):
        """Get application details"""
        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return {'message': 'Application not found'}, 404
        return application

    @blueprint.arguments(ApplicationSchema(partial=True))
    @blueprint.response(ApplicationSchema())
    def patch(self, args, application_id):
        """Edit application details"""
        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return {'message': 'Application not found'}, 404
        application.name = args.get('name', application.name)
        application.save()
        return application

    @blueprint.response(ApplicationSchema())
    def delete(self, application_id):
        """Delete application"""
        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            abort('Application not found', 404)
        application.delete()
        return application
