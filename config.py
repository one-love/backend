from local_config import BaseConfig
import os


class DevConfig(BaseConfig):
    DEBUG = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ONELOVE_MAIL_SUBJECT_PREFIX = '[OneLove] '
    ONELOVE_MAIL_SENDER = 'OneLove Admin <onelove@example.com>'


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    pass


configs = {
    'dev': DevConfig,
    'testing': TestConfig,
    'prod': ProdConfig,
    'default': ProdConfig
}
