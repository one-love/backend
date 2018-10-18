import eventlet
eventlet.monkey_patch()

import os  # noqa: E402

from config import configs  # noqa: E402
from onelove import cli, create_app  # noqa: E402


config_name = os.getenv('FLASK_ENV') or 'default'
app = create_app(configs[config_name])
cli.register(app)

if __name__ == '__main__':
    app.run()
