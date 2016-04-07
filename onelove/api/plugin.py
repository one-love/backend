from resources import ProtectedResource
from .namespaces import ns_plugin
from .fields.plugin import provider_fields
from flask import current_app as app


@ns_plugin.route('/providers', endpoint='providers')
class ProviderPluginListAPI(ProtectedResource):
    @ns_plugin.marshal_with(provider_fields)
    def get(self):
        """List provider plugins"""
        return [{'type': key} for key in app.config['PROVIDERS'].keys()]
