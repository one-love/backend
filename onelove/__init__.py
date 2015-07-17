from celery import Celery
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api
from flask_restful_swagger import swagger


class OneLove(object):
    api = None
    celery = Celery('onelove')
    db = MongoEngine()

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        OneLove.api = swagger.docs(Api(self.app), apiVersion='1.0')
        OneLove.celery.conf.update(app.config)
        OneLove.celery.set_default()
        OneLove.celery.set_current()
        OneLove.db.init_app(app)
        import resources
        resources.init(OneLove.api)
