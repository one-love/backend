from flask_jwt import current_identity
from .namespaces import ns_me
from .resources import ProtectedResource
from ..schemas import UserSchema


@ns_me.route('', endpoint='me')
class MeAPI(ProtectedResource):
    def get(self):
        """Logged in user details"""
        schema = UserSchema()
        response, errors = schema.dump(current_identity)
        if errors:
            abort(409, errors)
        return response
