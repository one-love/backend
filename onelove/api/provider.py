from flask_rest_api import Blueprint, abort

from ..models.provider import Provider, providers
from ..schemas.paging import PageInSchema, PageOutSchema, paginate
from ..schemas.provider import ProviderSchema
from .methodviews import ProtectedMethodView

blueprint = Blueprint('provider', 'provider')


@blueprint.route('/', endpoint='providers')
class ProviderListAPI(ProtectedMethodView):
    @blueprint.arguments(PageInSchema(), location='headers')
    @blueprint.response(PageOutSchema(ProviderSchema))
    def get(self, pagination):
        """List providers"""
        return paginate(Provider.objects.all(), pagination)

    @blueprint.arguments(ProviderSchema())
    @blueprint.response(ProviderSchema())
    def post(self, args):
        """Create provider"""
        provider_type = args.get('type', None)
        if provider_type is None:
            abort(409, message='Type is required')
        ProviderClass = providers.get(provider_type, None)
        if ProviderClass is None:
            abort(409, message='No such type')
        del args['type']
        provider = ProviderClass(**args)
        provider.save()
        return provider


@blueprint.route('/<provider_id>', endpoint='provider')
class ProviderAPI(ProtectedMethodView):
    @blueprint.response(ProviderSchema())
    def get(self, provider_id):
        """Get provider details"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        return provider

    @blueprint.arguments(ProviderSchema(partial=True))
    @blueprint.response(ProviderSchema())
    def patch(self, args, provider_id):
        """Edit provider details"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        provider.name = args.get('name', provider.name)
        provider.save()
        return provider

    @blueprint.response(ProviderSchema())
    def delete(self, provider_id):
        """Delete provider"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        provider.delete()
        return provider
