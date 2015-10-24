from flask.ext.restplus import Resource
from flask_jwt import current_identity
from ..models import User
from .fields import user_response as response_fields
from .namespaces import ns_me
from . import api
from resources import ProtectedResource

@ns_me.route('', endpoint='api/me')
class UserAPI(ProtectedResource):
    @api.marshal_with(response_fields)
    def get(self):
        """Show my details"""
        return current_identity

