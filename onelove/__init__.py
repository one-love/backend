from celery import Celery
from flask import Blueprint
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.restplus import apidoc
from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.security.utils import verify_password
from flask_jwt import JWT
from models import User, Role
from admin import admin
from flask_admin import helpers as admin_helpers


current_app = None


class OneLove(object):
    class Result(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    api = None
    blueprint = None
    celery = Celery('onelove')
    db = MongoEngine()
    mail = Mail()
    security = Security()
    user_datastore = None
    jwt = JWT()
    admin = admin

    def __init__(self, app=None):
        global current_app
        current_app = self
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        self.app = app

        from api import api_v0, api
        self.api = api

        self.blueprint = Blueprint(
            'onelove',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static/flarior',
        )

        self.app.register_blueprint(api_v0, url_prefix='/api/v0')
        self.app.register_blueprint(apidoc.apidoc)

        self.celery.conf.update(app.config)
        self.celery.set_default()
        self.celery.set_current()

        self.mail.init_app(app)

        self.db.init_app(app)
        self.admin.init_app(app)

        self.user_datastore = MongoEngineUserDatastore(
            OneLove.db,
            User,
            Role,
        )
        self.security.init_app(
            self.app,
            OneLove.user_datastore,
        )

        self.jwt.init_app(app)

        @app.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template,
                admin_view=admin.index_view,
                h=admin_helpers,
            )

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

    @jwt.identity_handler
    def identity(payload):
        try:
            user = User.objects.get(id=payload['identity'])
        except User.DoesNotExist:
            return None
        return user
