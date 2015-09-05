#!/usr/bin/env python
import os

from celery import current_app as celery
from flask import redirect, url_for, Flask, render_template
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
    return redirect(('api/v0/clusters'))

@app.route('/docs')
def docsr():
    return redirect(('api/v0/docs'))


@app.route('/api/v0/docs')
def docs():
    resource_list_url="/api/v0/spec/_/resource_list.json"
    base_url="/api/v0/spec/_/static/"
    return render_template(
        'swagger/index.html',
        base_url=base_url,
        resource_list_url=resource_list_url,
    )


if __name__ == '__main__':
    manager.run()
