from flask_jwt_extended import get_jwt_identity
from flask_rest_api import Blueprint, abort

from ..models.auth import User
from ..schemas.auth import UserSchema
from .methodviews import ProtectedMethodView

blueprint = Blueprint('me', 'me')


@blueprint.route('/', endpoint='me')
class MeAPI(ProtectedMethodView):
    @blueprint.response(UserSchema)
    def get(self):
        """Get my detail"""
        email = get_jwt_identity()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            abort(403, 'No such user, or wrong password')
        if not user.active:
            abort(403, 'No such user, or wrong password')
        return user
