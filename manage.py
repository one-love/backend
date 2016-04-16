#!/usr/bin/env python
import os

from flask import redirect, url_for
from flask_script import Manager
from onelove.tasks.monitor import create_monitor, thread

from onelove import OneLove
from onelove.utils import create_app


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
onelove = OneLove(app)
manager = Manager(app)


@manager.command
def runserver():
    onelove.socketio.run(
        app,
        host="0.0.0.0",
        use_reloader=True,
    )

onelove.collect.init_script(manager)


@app.route('/')
def index():
    return redirect(url_for(onelove.api.endpoint('doc')))


create_monitor()


if __name__ == '__main__':
    from onelove.utils import reload_celery, reload_frontend
    reload_celery(onelove.celery)
    reload_frontend()
    app.debug = True
    manager.run()
    thread.stop()
    thread = None
