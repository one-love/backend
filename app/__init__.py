from config import configs
from flask import Flask

from apiv1 import api
from models import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    api.init_app(app)
    db.init_app(app)

    return app
