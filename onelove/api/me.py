from flask_jwt import current_identity
from .fields import user_response as response_fields
from .namespaces import ns_me
from resources import ProtectedResource


@ns_me.route('', endpoint='me')
class UserAPI(ProtectedResource):
    @ns_me.marshal_with(response_fields)
    def get(self):
        """Show me details"""
        return current_identity
