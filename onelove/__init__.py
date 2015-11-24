from celery import Celery
from flask import send_from_directory
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

    admin = admin
    api = None
    celery = Celery('onelove')
    db = MongoEngine()
    jwt = JWT()
    mail = Mail()
    security = Security()
    toolbar = None
    user_datastore = None

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

        self.app.register_blueprint(api_v0, url_prefix='/api/v0')
        self.app.register_blueprint(apidoc.apidoc)

        OneLove.celery.conf.update(app.config)
        OneLove.celery.set_default()
        OneLove.celery.set_current()

        OneLove.mail.init_app(app)

        OneLove.db.init_app(app)
        OneLove.admin.init_app(app)

        OneLove.user_datastore = MongoEngineUserDatastore(
            OneLove.db,
            User,
            Role,
        )
        OneLove.security.init_app(
            self.app,
            OneLove.user_datastore,
        )

        OneLove.jwt.init_app(app)
        use_panel = self.app.config.get('DEBUG_TB_PANELS', False)
        if self.app.config.get('DEBUG_TB_PANELS', False):
            from flask_debugtoolbar import DebugToolbarExtension
            self.toolbar = DebugToolbarExtension(self.app)

        @app.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template,
                admin_view=admin.index_view,
                h=admin_helpers,
            )

        # OneLove static data
        @app.route('/backend/static/<path:filename>')
        def backend_static(filename):
            return send_from_directory(app.static_folder, filename)

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
