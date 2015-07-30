from flask.ext.restful import Resource, abort, reqparse, fields, marshal_with
from flask.ext.security.registerable import register_user
from mongoengine.queryset import NotUniqueError

from ..models import User


fields = {
    'email': fields.String,
    'first_name': fields.String,
    'id': fields.String,
    'last_name': fields.String,
    'password': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('email', type=str, required=True, location='json')


class UserListAPI(Resource):
    @marshal_with(fields)
    def get(self):
        return [user for user in User.objects.all()]

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
        return user


class UserAPI(Resource):
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

    @marshal_with(fields)
    def delete(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        user.delete()
        return user
