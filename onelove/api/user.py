from flask.ext.restful import abort, reqparse, fields, marshal_with
from flask.ext.security.registerable import register_user
from mongoengine.queryset import NotUniqueError
from flask_restful_swagger import swagger

from ..models import User
from resources import ProtectedResource


fields = {
    'email': fields.String,
    'first_name': fields.String,
    'id': fields.String,
    'last_name': fields.String,
    'password': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('email', type=str, required=True, location='json')
reqparse.add_argument('first_name', type=str, required=False, location='json')
reqparse.add_argument('last_name', type=str, required=False, location='json')
reqparse.add_argument('password', type=str, required=False, location='json')


@swagger.model
class UserListAPICreate:
    def __init__(self, email, password, first_name="NA", last_name="NA"):
        pass


class UserListAPI(ProtectedResource):
    @swagger.operation(summary='Get a users list')
    @marshal_with(fields)
    def get(self):
        return [user for user in User.objects.all()]

    @swagger.operation(
        notes='Create user',
        summary='Create the user',
        responseClass=UserListAPICreate.__name__,
        parameters=[
            {
                "method": "POST",
                "name": "user",
                "description": "User object to create a user",
                "required": True,
                "allowMultiple": False,
                "dataType": UserListAPICreate.__name__,
                "paramType": 'body'
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "New user is created."
            },
            {
                "code": 409,
                "message": "User with that email exists."
            }
        ]
        )
    @marshal_with(fields)
    def post(self):
        args = reqparse.parse_args()
        try:
            user = register_user(
                email=args.get('email'),
                first_name=args.get('first_name'),
                last_name=args.get('last_name'),
                password=args.get('password'),
            )
        except NotUniqueError:
            abort(409, error='User with that email exists')
        return user, 201


class UserAPI(ProtectedResource):
    @marshal_with(fields)
    def get(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        return user

    @marshal_with(fields)
    def put(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        args = reqparse.parse_args()
        user.email = args.get('email')
        user.save()
        return user

    @swagger.operation(summary='Delete a user')
    @marshal_with(fields)
    def delete(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        user.delete()
        return user
