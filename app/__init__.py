# from .models import db
from .apiv1 import api
from flask import Flask
from .config import configs


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    api.init_app(app)

    return app
