from flask.ext.restplus import Resource
from flask.ext.restful import request
from flask_jwt import _jwt, JWTError
from . import api
from .namespaces import ns_auth
from .fields import auth_fields, token_response


parser = api.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('password', type=str, required=False, location='json')


@ns_auth.route('/tokens', endpoint='auth.token')
@api.doc(body=auth_fields)
class AuthAPI(Resource):
    @api.response(401, 'Invalid credentials')
    @api.doc(security=None)
    @api.marshal_with(token_response, code=200, description='Get a token.')
    def post(self):
        """Authenticates and generates a token."""
        args = parser.parse_args()
        data = request.get_json(force=True)
        username = args.get('email')
        password = args.get('password')
        criterion = [username, password, len(data) == 2]

        if not all(criterion):
            raise JWTError('Bad Request', 'Invalid credentials')

        identity = _jwt.authentication_callback(username, password)

        if identity:
            access_token = _jwt.jwt_encode_callback(identity)
            token = {
                "token": access_token
            }
            return token
        else:
            raise JWTError('Bad Request', 'Invalid credentials')
