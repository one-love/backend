from celery import Celery
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api
from flask.ext.security import Security, MongoEngineUserDatastore
from flask_restful_swagger import swagger


class OneLove(object):
    api = None
    celery = Celery('onelove')
    db = MongoEngine()
    mail = Mail()
    security = Security()
    user_datastore = None

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
