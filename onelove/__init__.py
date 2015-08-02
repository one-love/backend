from celery import Celery
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api
from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.security.utils import verify_password
from flask_jwt import JWT
from flask_restful_swagger import swagger

from models import User


class Result(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class OneLove(object):
    api = None
    celery = Celery('onelove')
    db = MongoEngine()
    mail = Mail()
    security = Security()
    user_datastore = None
    jwt = JWT()

    def __init__(self, app=None):
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        self.app = app
        OneLove.api = swagger.docs(
            Api(
                self.app,
                prefix='/api/v1.0'
            ),
            apiVersion='1.0'
        )
        OneLove.celery.conf.update(app.config)
        OneLove.celery.set_default()
        OneLove.celery.set_current()

        OneLove.mail.init_app(app)

        OneLove.db.init_app(app)

        from models import User, Role
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

        OneLove.jwt.init_app(app)

    @jwt.authentication_handler
    def authenticate(username, password):
        from models import User
        result = None
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

    @jwt.user_handler
    def load_user(payload):
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return None
        return user
