from .resources import ProtectedResource
from .namespaces import ns_plugin
from .fields.plugin import provider_fields
from flask import current_app as app
from flask_restplus import abort


@ns_plugin.route('/providers', endpoint='providers')
class ProviderPluginListAPI(ProtectedResource):
    @ns_plugin.marshal_with(provider_fields)
    def get(self):
        """List provider plugins"""
        result = []
        for key in app.config['PROVIDERS'].keys():
            Provider = app.config['PROVIDERS'][key]
            provider = {
                'type': Provider.type,
                'properties': Provider.fields(),
            }
            result.append(provider)
        return result


@ns_plugin.route('/providers/<providerType>', endpoint='provider')
class ProviderPluginListAPI(ProtectedResource):
    @ns_plugin.marshal_with(provider_fields)
    def get(self, providerType):
        """Details about provider plugin"""
        Provider = app.config['PROVIDERS'].get(providerType, None)
        if Provider is None:
            abort(404, 'No such provider type')
        provider = {
            'type': Provider.type,
            'properties': Provider.fields(),
        }
        return provider
