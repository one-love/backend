#!/usr/bin/env python
import os

from flask import redirect, url_for, request
from flask_script import Manager
from flask_socketio import join_room, disconnect
from gevent import Greenlet

from onelove import OneLove
from onelove.monitor import monitor
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
        debug=True,
        use_reloader=True,
    )

onelove.collect.init_script(manager)


@app.route('/')
def index():
    return redirect(url_for(onelove.api.endpoint('doc')))


@onelove.socketio.on('connect')
def on_connect():
    from onelove.models import User
    token = request.args.get('token', None)
    request.namespace = '/onelove'
    if token is None:
        disconnect()
        return

    current_identity = None
    try:
        current_identity = onelove.jwt.jwt_decode_callback(token)
    except:
        disconnect()

    if current_identity is None:
        disconnect()
        return
    user = User.objects.get(id=current_identity['identity'])
    join_room(str(user.id))


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    Greenlet.spawn(monitor)


if __name__ == '__main__':
    manager.run()
