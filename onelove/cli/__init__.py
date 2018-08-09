import click
from flask_security.utils import encrypt_password
from onelove.models.auth import User


def register(app):
    @app.cli.command()
    @click.option('-p', '--port', default=5000, help='Dev server port')
    def runserver(port):
        """Run development server with SocketIO"""
        app.socketio.run(
            app,
            host='0.0.0.0',
            debug=True,
            use_reloader=True,
            port=port
        )
