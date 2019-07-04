from flask_rest_api import Blueprint

from ..models.auth import User
from ..schemas.auth import UserSchema
from ..schemas.paging import PagingSchema
from .methodviews import ProtectedMethodView

blueprint = Blueprint('user', 'user')


@blueprint.route('/', endpoint='users')
class UserListAPI(ProtectedMethodView):
    @blueprint.arguments(PagingSchema(), location='headers')
    @blueprint.response(UserSchema(many=True))
    def get(self, pagination):
        """List users"""
        return User.objects.all()

    @blueprint.arguments(UserSchema)
    @blueprint.response(UserSchema)
    def post(self, args):
        """Create user"""
        user = User(**args)
        user.save()
        return user


@blueprint.route('/<user_id>', endpoint='user')
class UserAPI(ProtectedMethodView):
    @blueprint.response(UserSchema)
    def get(self, user_id):
        """Get user details"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {'message': 'User not found'}, 404
        return user

    @blueprint.arguments(UserSchema(partial=True))
    @blueprint.response(UserSchema)
    def patch(self, args, user_id):
        """Edit user"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {'message': 'User not found'}, 404
        for arg in args:
            setattr(user, arg, args[arg])
        user.save()
        return user

    @blueprint.response(UserSchema)
    def delete(self, user_id):
        """Delete user"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {'message': 'User not found'}, 404
        user.delete()
        return user
