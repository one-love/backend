try:
    from local_config import Config
except ModuleNotFoundError:
    from common_config import CommonConfig as Config


class DevConfig(Config):
    DEBUG = True
    JWT_COOKIE_SECURE = False
    SECURITY_SEND_REGISTER_EMAIL = False


class TestConfig(Config):
    TESTING = True
    JWT_COOKIE_SECURE = False


class TestConfigCI(TestConfig):
    MONGODB_HOST = '127.0.0.1'


class ProdConfig(Config):
    pass


configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'testingci': TestConfigCI,
    'production': ProdConfig,
    'default': ProdConfig,
}
