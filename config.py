from datetime import timedelta
import os


try:
    from local_config import BaseConfig
except ImportError:
    class BaseConfig(object):
        SECRET_KEY = 'top-secret'
        MONGODB_HOST = 'mongodb',


class Config(BaseConfig):
    DEBUG = False
    SECURITY_PASSWORD_SALT = 'tilda'
    SECRET_KEY = 'iQfPvB6sZaNHqVFI5CJa9rM1xOEVHKIM0LwifT04yLsPlZhSSvaDuZXOgJFSpJVq'
    SECURITY_TRACKABLE = False
    JWT_EXPIRATION_DELTA = timedelta(days=7)

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SECURITY_SEND_REGISTER_EMAIL = False


class TestConfig(Config):
    TESTING = True


class ProdConfig(Config):
    pass


configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': ProdConfig,
}
