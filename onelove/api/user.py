from flask.ext.security.registerable import register_user
from mongoengine.queryset import NotUniqueError
from mongoengine.errors import ValidationError
from . import api
from .namespaces import ns_user
from .fields import user_body as body_fields
from .fields import user_response as response_fields


from ..models import User
from resources import ProtectedResource


parser = api.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('first_name', type=str, required=False, location='json')
parser.add_argument('last_name', type=str, required=False, location='json')
parser.add_argument('password', type=str, required=False, location='json')


@ns_user.route('', endpoint='users')
class UserListAPI(ProtectedResource):
    @api.marshal_with(response_fields)
    def get(self):
        """List users"""
        return [user for user in User.objects.all()]

    @api.doc(
        model=response_fields,
        body=body_fields,
        responses={
            409: 'User with that email exists',
            422: 'Validation error'
        }
    )
    @api.marshal_with(response_fields)
    def post(self):
        """Create user"""
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
        except (ValidationError):
            api.abort(422, error='ValidationError')
        return user, 201


@ns_user.route('/<id>', endpoint='user')
class UserAPI(ProtectedResource):
    @api.marshal_with(response_fields)
    def get(self, id):
        """Show user details"""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            api.abort(404, error='User does not exist')

        return user

    @api.expect(body_fields)
    @api.marshal_with(response_fields)
    def put(self, id):
        """Update user"""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            api.abort(404, error='User does not exist')

        args = parser.parse_args()
        user.email = args.get('email')
        user.save()
        return user

    @api.marshal_with(response_fields)
    def delete(self, id):
        """Delete user."""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            api.abort(404, error='User does not exist')
        user.delete()
        return user
