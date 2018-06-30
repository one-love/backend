from datetime import timedelta
from onelove.plugin import load_hosting_providers, load_knowledge_sources
from plugins import HOSTING_PROVIDERS, KNOWLEDGE_SOURCES
import os


BACKEND_PATH = os.path.dirname(os.path.abspath(__file__))
BACKEND_APP = os.path.basename(BACKEND_PATH)

try:
    from local_config import BaseConfig
except ImportError:
    class BaseConfig(object):
        SECRET_KEY = 'top-secret'
        MONGODB_HOST = 'mongodb'


class Config(BaseConfig):
    DEBUG = False
    JWT_EXPIRATION_DELTA = timedelta(days=7)
    KNOWLEDGE_SOURCES = load_knowledge_sources(KNOWLEDGE_SOURCES)
    MONGODB_DB = 'onelove'
    PROVIDERS = load_hosting_providers(HOSTING_PROVIDERS)
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'COmwUar8X1s4NrNN'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_URL_PREFIX = "/admin"

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
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
        'flask_debug_api.BrowseAPIPanel'
    ]


class TestConfig(Config):
    TESTING = True
    MONGODB_DB = 'test'


class ProdConfig(Config):
    pass


configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': ProdConfig
}
