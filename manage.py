#!/usr/bin/env python
import os

from celery import current_app as celery
from flask import render_template, request, redirect, url_for
from flask_script import Manager, Server

from onelove import OneLove
from onelove.utils import create_app


config_name = os.getenv('FLASK_CONFIG') or 'default'
onelove = OneLove(create_app(config_name))
manager = Manager(onelove.app)
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


@onelove.app.route('/')
def index():
    return redirect(url_for(onelove.api.endpoint('doc')))


if __name__ == '__main__':
    from onelove.utils import reload_frontend
    reload_frontend()
    manager.run()
