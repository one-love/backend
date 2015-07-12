import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # MARSHMALLOW_STRICT = True
    # MARSHMALLOW_DATEFORMAT = 'rfc'
    MONGODB_HOST = os.environ.get('MONGODB_PORT_27017_TCP_ADDR')
    MONGODB_DB = 'onelove'
    BROKER_URL = 'amqp://guest@%s//' % os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR')
    CELERY_RESULT_BACKEND = 'rpc://'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    pass


configs = {
    'dev': DevConfig,
    'testing': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
