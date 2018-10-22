from common_config import TestConfig as Config


class TestConfig(Config):
    MONGODB_SETTINGS = {
        'host': 'localhost',
    }
