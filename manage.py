#!/usr/bin/env python
import os

from flask import redirect, url_for, request
from flask_script import Manager
from onelove.tasks.monitor import create_monitor, thread
from flask_socketio import join_room, disconnect

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


@onelove.socketio.on('connect')
def on_connect():
    from onelove.models import User
    token = request.args.get('token', None)
    request.namespace = '/onelove'
    if token is None:
        disconnect()
        return
    try:
        current_identity = onelove.jwt.jwt_decode_callback(token)
    except:
        disconnect()
        return
    if current_identity is None:
        disconnect()
        return
    user = User.objects.get(id=current_identity['identity'])
    join_room(user.id)


if __name__ == '__main__':
    app.debug = True
    manager.run()
    thread.stop()
    thread = None
