#!/usr/bin/env python
import os

from celery import current_app as celery
from flask import redirect, url_for
from flask_script import Manager, Server

from onelove import OneLove
from onelove.utils import create_app


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
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
onelove.collect.init_script(manager)

from onelove.tasks import *


@app.route('/')
def index():
    return redirect(url_for(onelove.api.endpoint('doc')))


if __name__ == '__main__':
    from onelove.utils import reload_celery, reload_frontend
    reload_celery(celery)
    reload_frontend()
    manager.run()
