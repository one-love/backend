from flask.ext.restful import reqparse, fields, marshal_with, Resource, request
from flask_restful_swagger import swagger
from flask_jwt import _jwt, JWTAuthView, JWTError


fields = {
    'token': fields.String,
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('email', type=str, required=True, location='json')
reqparse.add_argument('password', type=str, required=False, location='json')


def generate_token(user):
    """Generate a token for a user.
    """
    payload = _jwt.payload_callback(user)
    token = _jwt.encode_callback(payload)
    return token


@swagger.model
class AuthAPIpost:
    def __init__(self, email, password):
        pass


class AuthAPI(JWTAuthView, Resource):
    @swagger.operation(
        summary='Get a token.',
        responseClass=AuthAPIpost.__name__,
        parameters=[
            {
                "method": "POST",
                "name": "user",
                "description": "User credentials.",
                "required": True,
                "allowMultiple": False,
                "dataType": AuthAPIpost.__name__,
                "paramType": 'body'
            }
            ],
        responseMessages=[
            {
                "code": 400,
                "message": "Invalid credentials."
            }
            ]
        )
    @marshal_with(fields)
    def post(self):
        args = reqparse.parse_args()
        data = request.get_json(force=True)
        username = args.get('email')
        password = args.get('password')
        criterion = [username, password, len(data) == 2]

        if not all(criterion):
            raise JWTError(
                'Bad Request', 'Missing required credentials', status_code=400
            )

        user = _jwt.authentication_callback(username, password)

        if user:
            token = {
                "token": generate_token(user)
            }
            return token
        else:
            raise JWTError('Bad Request', 'Invalid credentials')
