from local_config import BaseConfig
import os


class DevConfig(BaseConfig):
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
        'flask.ext.mongoengine.panels.MongoDebugPanel',
    ]


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    SECURITY_POST_LOGIN_VIEW = "/admin/"
    pass


configs = {
    'dev': DevConfig,
    'testing': TestConfig,
    'prod': ProdConfig,
    'default': ProdConfig
}
