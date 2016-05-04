from celery import Celery
from flask import Blueprint
from flask_collect import Collect
from flask_cors import CORS
from flask_jwt import JWT
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_restplus import apidoc
from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import verify_password
from flask_socketio import SocketIO
from .models import User, Role
from gevent import monkey


monkey.patch_all()


current_app = None


class OneLove(object):
    class Result(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    api = None
    app = None
    blueprint = None
    celery = Celery('onelove')
    collect = Collect()
    db = MongoEngine()
    jwt = JWT()
    mail = Mail()
    security = Security()
    socketio = None
    toolbar = None
    user_datastore = None

    def __init__(self, app=None):
        if app is not None:
            if app.config['DEBUG']:
                from flask_admin import Admin, AdminIndexView
                self.cors = CORS()
                self.admin = Admin(
                    name='One Love',
                    base_template='admin_master.html',
                    template_mode='bootstrap3',
                    index_view=AdminIndexView(
                        template='admin/onelove_index.html',
                    ),
                )
            self.init_app(app)

    def init_app(self, app):
        global current_app
        current_app = self
        self.app = app
        if app.config['DEBUG']:
            self.cors.init_app(
                self.app,
                resources={r'/api/*': {'origins': '*'}},
            )

        from api import api_v0, api
        self.api = api

        self.blueprint = Blueprint(
            'onelove',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static/onelove',
        )
        self.app.register_blueprint(self.blueprint)

        self.app.register_blueprint(api_v0, url_prefix='/api/v0')
        self.app.register_blueprint(apidoc.apidoc)

        self.celery.conf.update(self.app.config)
        self.celery.set_default()
        self.celery.set_current()

        self.mail.init_app(self.app)

        self.db.init_app(self.app)

        self.user_datastore = MongoEngineUserDatastore(
            self.db,
            User,
            Role,
        )
        self.security.init_app(
            self.app,
            self.user_datastore,
        )

        if app.config['DEBUG']:
            from .admin import register_admin_views
            register_admin_views(self.admin)
            self.admin.init_app(self.app)

        self.jwt.init_app(self.app)
        self.collect.init_app(self.app)

        if self.app.config.get('DEBUG_TB_PANELS', False):
            from flask_debugtoolbar import DebugToolbarExtension
            from flask_debug_api import DebugAPIExtension
            self.toolbar = DebugToolbarExtension(self.app)
            self.toolbar = DebugAPIExtension(self.app)

        if self.app.config.get('DEBUG', False):
            from flask_admin import helpers as admin_helpers

            @self.app.context_processor
            def security_context_processor():
                return dict(
                    admin_base_template=self.admin.base_template,
                    admin_view=self.admin.index_view,
                    h=admin_helpers,
                )

        self.socketio = SocketIO(self.app, logger=True)
        self.app.onelove = self

    @jwt.authentication_handler
    def authenticate(username, password):
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
            user = None
        return user
