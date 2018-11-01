import os

from flask import Flask
from flask_collect import Collect
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security
from flask_socketio import SocketIO

from .api import create_api
from .models.auth import Role, User
from .socket import SocketThread
from .tasks.celery import make_celery


def create_app(config, app=None):
    class Result(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    if app is None:
        app = Flask(__name__)
        app.config.from_object(config)

    app.collect = Collect(app)
    app.celery = make_celery(app)
    app.db = MongoEngine(app)
    app.user_datastore = MongoEngineUserDatastore(
        app.db,
        User,
        Role,
    )
    app.security = Security(app, app.user_datastore)
    create_api(app)
    app.socketio = SocketIO(app, logger=True)

    werkzeug = os.environ.get('WERKZEUG_RUN_MAIN', 'true')
    if werkzeug == 'true':
        app.socket_thread = SocketThread(
            app.socketio,
            app.config['REDIS_HOST']
        )
        app.socket_thread.start()
    return app
