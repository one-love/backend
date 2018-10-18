import click
from celery.bin import worker as w
from flask import current_app
from flask.cli import AppGroup

celery = AppGroup('celery', short_help='Manage celery worker')


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

    @celery.command()
    def start():
        worker = w.worker(app=current_app.celery)
        worker.run(
            loglevel=current_app.config['CELERY_LOG_LEVEL'],
            traceback=True,
            pool_cls='eventlet',
        )

    app.cli.add_command(celery)
