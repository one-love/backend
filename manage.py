#!/usr/bin/env python
import os

from celery import current_app as celery
from flask import redirect, url_for, Flask
from flask.ext.script import Manager, Server

from onelove import OneLove
from config import configs


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = Flask(__name__)
app.config.from_object(configs[config_name])
onelove = OneLove(app)
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True
    )
)


@app.route('/')
def index():
    return redirect(url_for('api/clusters'))


if __name__ == '__main__':
    manager.run()
