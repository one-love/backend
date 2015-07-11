from flask import Flask
from config import configs
from flask.ext.mongoengine import MongoEngine
from flask_restful_swagger import swagger
from flask.ext.restful import Api


db = MongoEngine()
api = swagger.docs(Api(), apiVersion='0.1')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    api.init_app(app)
    db.init_app(app)

    return app
