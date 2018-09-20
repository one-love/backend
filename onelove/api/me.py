from flask_jwt_extended import get_jwt_identity
from flask_restplus import abort

from ..models.auth import User
from .namespaces import ns_me
from .resources import ProtectedResource
from .schemas import UserSchema


@ns_me.route('', endpoint='me')
@ns_me.response(404, 'User not found')
class MeAPI(ProtectedResource):
    def get(self):
        """Get my details"""
        email = get_jwt_identity()
        user = User.objects.get(email=email)
        if not user or not user.active:
            abort(403, 'No such user, or wrong password')
        schema = UserSchema()
        response, errors = schema.dump(user)
        if errors:
            abort(409, errors)
        return response
