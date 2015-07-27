from flask.ext.restful import Resource, reqparse, fields, marshal_with

from ..models import User


fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
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
        user.save()
        return user


class UserAPI(Resource):
    @marshal_with(fields)
    def get(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return {'message': 'User does not exist'}
        return user

    @marshal_with(fields)
    def put(self, id):
        args = reqparse.parse_args()
        user = User.objects.get(id=id)
        user.email = args.get('email')
        user.save()
        return user

    def delete(self, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return {'message': 'User does not exist'}
        user.delete()
        return {'message': 'deleted'}
