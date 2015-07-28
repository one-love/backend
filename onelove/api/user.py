from flask.ext.restful import Resource, reqparse, fields, marshal_with

from ..models import User
from ..email import send_email


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
        user = User(
            email=args.get('email'),
            password=args.get('password'),
        )
        send_email(user.email,
                   'Confirm Your Account',
                   'mail/confirm',
                   user=user,
                   )
        user.save()
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

    def delete(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            abort(404, error='User does not exist')
        user.delete()
        return {'message': 'deleted'}
