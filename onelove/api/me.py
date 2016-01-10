from flask_jwt import current_identity
from .fields import user_response as response_fields
from .namespaces import ns_me
from . import api
from resources import ProtectedResource


@ns_me.route('', endpoint='api/me')
class UserAPI(ProtectedResource):
    @api.marshal_with(response_fields)
    def get(self):
        """Show me details"""
        return current_identity
