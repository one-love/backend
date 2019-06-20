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
        schema = UserSchema()
        data, errors = schema.load(args)
        if errors:
            return errors, 409
        account = User(**data)
        account.save()
        return account


@blueprint.route('/<id>', endpoint='user')
class UserAPI(ProtectedMethodView):
    @blueprint.response(UserSchema)
    def get(self, id):
        """Get user details"""
        try:
            account = User.objects.get(id=id)
        except User.DoesNotExist:
            return {'message': 'User not found'}, 404
        return account
