#!/usr/bin/env python
import os

from flask import redirect, url_for, Flask
from flask.ext.script import Manager, Server

from onelove import init_app, celery


config = os.getenv('FLASK_CONFIG') or 'default'
app = Flask(__name__)
init_app(app, config)
celery.set_default()
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True
    )
)


@manager.app.route('/')
def index():
    return redirect(url_for('servers'))


if __name__ == '__main__':
    manager.run()
