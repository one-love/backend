from flask import Blueprint
from flask.ext.restplus import Api

api_auth = Blueprint('api', __name__)

authorizations = {
    'token': {
        'type': 'Authorization',
        'in': 'header',
        'name': 'Bearer'
    }
}

api = Api(api_auth, version='0', title='Todo API',
            description='A simple TODO API',
            authorizations=authorizations,
            security='token'
        )


from . import auth
from . import user
