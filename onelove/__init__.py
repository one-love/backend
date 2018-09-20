from flask import Flask, Blueprint
from flask_collect import Collect
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_restplus import apidoc
from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import verify_password
from .api import create_api


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

    from .models.auth import User, Role
    app.db = MongoEngine(app)
    app.user_datastore = MongoEngineUserDatastore(
        app.db,
        User,
        Role,
    )
    app.security = Security(app, app.user_datastore)
    create_api(app)

    return app
