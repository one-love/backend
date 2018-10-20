from flask import current_app
from flask_restplus import abort

from ..models.provider import Provider
from .namespaces import ns_provider
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ProviderSchema


@ns_provider.route('', endpoint='providers')
class ProviderListAPI(ProtectedResource):
    @ns_provider.expect(parser)
    def get(self):
        """Get list of providers"""
        return paginate(Provider.objects(), ProviderSchema())

    @ns_provider.expect(ProviderSchema.fields())
    def post(self):
        """Create provider"""
        schema = ProviderSchema()
        provider, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        provider.save()
        response, errors = schema.dump(provider)
        if errors:
            return errors, 409
        return response


@ns_provider.route('/<provider_id>', endpoint='provider')
class ProviderAPI(ProtectedResource):
    def get(self, provider_id):
        """Get provider details"""
        try:
            provider = Provider.objects().get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, 'No such provider')
        schema = ProviderSchema()
        response, errors = schema.dump(provider)
        if errors:
            return errors, 409
        return response

    @ns_provider.expect(ProviderSchema.fields(required=False))
    def patch(self, provider_id):
        """Change provider details"""
        try:
            provider = Provider.objects().get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, 'No such provider')
        schema = ProviderSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        provider.name = data.name or provider.name
        response, errors = schema.dump(provider)
        if errors:
            return errors, 409
        provider.save()
        return response

    def delete(self, provider_id):
        """Delete the provider"""
        try:
            provider = Provider.objects().get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, 'No such provider')
        schema = ProviderSchema()
        response, errors = schema.dump(provider)
        if errors:
            return errors, 409
        provider.delete()
        return response
