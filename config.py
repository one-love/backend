from datetime import timedelta
import os


BACKEND_PATH = os.path.dirname(os.path.abspath(__file__))
BACKEND_APP = os.path.basename(BACKEND_PATH)

try:
    from local_settings import BaseConfig
except ImportError:
    class BaseConfig(object):
        SECRET_KEY = 'top-secret'
        pass


class Config(BaseConfig):
    DEBUG = False
    FRONTEND_LIVERELOAD = False
    MONGODB_DB = 'onelove'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'COmwUar8X1s4NrNN'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_POST_LOGIN_VIEW = '/admin/'
    SECURITY_POST_LOGOUT_VIEW = '/admin/'
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    JWT_EXPIRATION_DELTA = timedelta(days=7)

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    FRONTEND_LIVERELOAD = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ONELOVE_MAIL_SUBJECT_PREFIX = '[OneLove] '
    ONELOVE_MAIL_SENDER = 'OneLove Admin <onelove@example.com>'
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_PANELS = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel',
    ]


class TestConfig(Config):
    TESTING = True


class ProdConfig(Config):
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'


configs = {
    'dev': DevConfig,
    'testing': TestConfig,
    'prod': ProdConfig,
    'default': ProdConfig
}
