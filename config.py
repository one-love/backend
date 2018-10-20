try:
    from local_config import DevConfig
except ImportError:
    from common_config import DevConfig

try:
    from local_config import TestConfig
except ImportError:
    from common_config import TestConfig

try:
    from local_config import TestCIConfig
except ImportError:
    from common_config import TestCIConfig

try:
    from local_config import ProdConfig
except ImportError:
    from common_config import ProdConfig

configs = {
    'default': ProdConfig,
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig,
    'testingci': TestCIConfig,
}
