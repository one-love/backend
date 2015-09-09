from flask.ext.restplus import Resource
from flask.ext.restful import request
from flask_jwt import _jwt, JWTAuthView, JWTError
from . import api
from .namespaces import ns_auth
from .fields import auth_fields, token_response


parser = api.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('password', type=str, required=False, location='json')


def generate_token(user):
    """Generate a token for a user.
    """
    payload = _jwt.payload_callback(user)
    token = _jwt.encode_callback(payload)
    return token


@ns_auth.route('/token', endpoint='auth/token')
@api.doc(body=auth_fields)
class AuthAPI(JWTAuthView, Resource):
    @api.response(400, 'Invalid credentials')
    @api.doc(security=None)
    @api.marshal_with(token_response, code=200, description='Get a token.')
    def post(self):
        args = parser.parse_args()
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
