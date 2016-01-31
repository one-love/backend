from flask import Flask
from config import configs


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    return app
