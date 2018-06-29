import os
from config import configs
from onelove import create_app


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(configs[config_name])


if __name__ == '__main__':
    app.run()

