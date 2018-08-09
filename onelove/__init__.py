from flask import Flask, Blueprint
from flask_collect import Collect
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_jwt import JWT
from flask_restplus import apidoc
from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import verify_password
from werkzeug.security import safe_str_cmp


def create_app(config, app=None):
    class Result(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    if app is None:
        app = Flask(__name__)
        app.config.from_object(config)

    debug = app.config.get('DEBUG', False)
    if debug:
        CORS(app)
    app.collect = Collect(app)

    from .api import api_v0, api
    app.api = api
    app.register_blueprint(api_v0)
    app.register_blueprint(apidoc.apidoc)

    from .models.auth import User, Role
    app.db = MongoEngine(app)
    app.user_datastore = MongoEngineUserDatastore(
        app.db,
        User,
        Role,
    )
    app.security = Security(app, app.user_datastore)

    def authenticate(username, password):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        result = Result(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        if verify_password(password, user.password):
            return result

    def identity(payload):
        try:
            user = User.objects.get(id=payload['identity'])
        except User.DoesNotExist:
            user = None
        return user

    app.jwt = JWT(app, authenticate, identity)

    from .api import auth, user, me

    return app
