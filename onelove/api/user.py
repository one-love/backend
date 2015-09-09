from flask.ext.restplus import abort, reqparse, fields, marshal_with
from flask.ext.security.registerable import register_user
from mongoengine.queryset import NotUniqueError
from . import api

from ..models import User
from resources import ProtectedResource


ns_user = api.namespace('user', description='Users operations')

users_fields = api.model('User', {
        'email': fields.String(
            description='The email',
            required=True,
            default='admin@example.com'
        ),
        'first_name': fields.String,
        'last_name': fields.String,
        'password': fields.String(
            description='Password',
            required=True,
            default='Sekrit'
        ),
    }
)

get_users_fields = api.extend('Get Users', users_fields, {
        'id': fields.String,
    }
)


parser = api.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('first_name', type=str, required=False, location='json')
parser.add_argument('last_name', type=str, required=False, location='json')
parser.add_argument('password', type=str, required=False, location='json')

@ns_user.route('/list', endpoint='user/list')
class UserListAPI(ProtectedResource):
    @api.marshal_with(get_users_fields)
    def get(self):
        return [user for user in User.objects.all()]

    @api.expect(users_fields)
    @api.marshal_with(users_fields)
    def post(self):
        args = parser.parse_args()
        try:
            user = register_user(
                email=args.get('email'),
                first_name=args.get('first_name'),
                last_name=args.get('last_name'),
                password=args.get('password'),
            )
        except NotUniqueError:
            abort(409, error='User with that email exists')
        return user


@ns_user.route('/<id>', endpoint='user/user')
class UserAPI(ProtectedResource):
    @api.marshal_with(users_fields)
    def get(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        return user

    @api.expect(users_fields)
    @api.marshal_with(users_fields)
    def put(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        args = parse.parse_args()
        user.email = args.get('email')
        user.save()
        return user

    @api.marshal_with(users_fields)
    def delete(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        user.delete()
        return user
