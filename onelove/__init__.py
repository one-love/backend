from celery import Celery
from flask import Blueprint
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api
from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.security.utils import verify_password
from flask_jwt import JWT, JWTError
from flask_restful_swagger import swagger

from models import User, Role


current_app = None
blueprint_v0 = Blueprint('blueprint_v0', __name__)


class ErrorFriendlyApi(Api):
    def error_router(self, original_handler, e):
        if type(e) is JWTError:
            return original_handler(e)
        else:
            return super(
                ErrorFriendlyApi,
                self
            ).error_router(
                original_handler,
                e
            )


class OneLove(object):
    class Result(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    api = None
    celery = Celery('onelove')
    db = MongoEngine()
    mail = Mail()
    security = Security()
    user_datastore = None
    jwt = JWT()

    def __init__(self, app=None):
        global current_app
        current_app = self
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        self.app = app
        OneLove.api = swagger.docs(
            ErrorFriendlyApi(
                blueprint_v0
            ),
            apiVersion='0',
            api_spec_url='/spec',
            description='OneLove API',
            swaggerVersion='2.0'
        )
        OneLove.celery.conf.update(app.config)
        OneLove.celery.set_default()
        OneLove.celery.set_current()

        OneLove.mail.init_app(app)

        OneLove.db.init_app(app)

        OneLove.user_datastore = MongoEngineUserDatastore(
            OneLove.db,
            User,
            Role,
        )
        OneLove.security.init_app(
            self.app,
            OneLove.user_datastore,
        )

        import urls
        urls.init(OneLove.api)

        self.app.register_blueprint(blueprint_v0, url_prefix='/api/v0')
        OneLove.jwt.init_app(app)

    @jwt.authentication_handler
    def authenticate(username, password):
        result = None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        result = OneLove.Result(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        if verify_password(password, user.password):
            return result

    @jwt.user_handler
    def load_user(payload):
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return None
        return user
