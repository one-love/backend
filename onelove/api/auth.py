from flask.ext.restful import reqparse, fields, marshal_with, Resource
from flask_restful_swagger import swagger
import flask_jwt


fields = {
    'token': fields.String,
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('email', type=str, required=True, location='json')
reqparse.add_argument('password', type=str, required=False, location='json')


def generate_token(user):
    """Generate a token for a user.
    """
    payload = flask_jwt._jwt.payload_callback(user)
    token = flask_jwt._jwt.encode_callback(payload)
    return token


@swagger.model
class LoginAPIpost:
    def __init__(self, email, password):
        pass


class LoginAPI(flask_jwt.JWTAuthView, Resource):
    @swagger.operation(
        summary='Login a user',
        responseClass=LoginAPIpost.__name__,
        parameters=[
            {
                "method": "POST",
                "name": "user",
                "description": "Login",
                "required": True,
                "allowMultiple": False,
                "dataType": LoginAPIpost.__name__,
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
        data = flask_jwt.request.get_json(force=True)
        username = args.get('email')
        password = args.get('password')
        criterion = [username, password, len(data) == 2]

        if not all(criterion):
            raise flask_jwt.JWTError(
                'Bad Request', 'Missing required credentials', status_code=400
            )

        user = flask_jwt._jwt.authentication_callback(username, password)

        if user:
            token = {
                "token": generate_token(user)
            }
            return token
        else:
            raise flask_jwt.JWTError('Bad Request', 'Invalid credentials')
