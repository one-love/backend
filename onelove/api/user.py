from flask.ext.security.registerable import register_user
from mongoengine.queryset import NotUniqueError
from mongoengine.errors import ValidationError
from . import api
from .namespaces import ns_user
from .fields import user_fields as fields
from .fields import get_user_fields as get_fields

from ..models import User
from resources import ProtectedResource


parser = api.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('first_name', type=str, required=False, location='json')
parser.add_argument('last_name', type=str, required=False, location='json')
parser.add_argument('password', type=str, required=False, location='json')


@ns_user.route('', endpoint='api/users')
class UserListAPI(ProtectedResource):
    @api.marshal_with(get_fields)
    def get(self):
        """Get list of users."""
        return [user for user in User.objects.all()]

    @api.expect(fields)
    @api.marshal_with(fields)
    def post(self):
        """Create the user."""
        args = parser.parse_args()
        try:
            user = register_user(
                email=args.get('email'),
                first_name=args.get('first_name'),
                last_name=args.get('last_name'),
                password=args.get('password'),
            )
        except NotUniqueError:
            api.abort(409, error='User with that email exists')
        return user, 201


@ns_user.route('/<id>', endpoint='api/user')
class UserAPI(ProtectedResource):
    @api.marshal_with(fields)
    def get(self, id):
        """Get informations for the user"""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            api.abort(404, error='User does not exist')

        return user

    @api.expect(fields)
    @api.marshal_with(fields)
    def put(self, id):
        """Change user informations"""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            api.abort(404, error='User does not exist')

        args = parser.parse_args()
        user.email = args.get('email')
        user.save()
        return user

    @api.marshal_with(fields)
    def delete(self, id):
        """Delete the user."""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            api.abort(404, error='User does not exist')
        user.delete()
        return user
