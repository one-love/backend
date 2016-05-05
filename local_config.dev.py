class BaseConfig(object):
    MONGODB_HOST = 'db'
    CELERY_RESULT_BACKEND = 'mongodb://db/'
    CELERY_MONGODB_BACKEND_SETTINGS = {
        'database': 'onelove',
    }

    BROKER_URL = 'amqp://guest@mq//'
    SECRET_KEY = 'tX8oLQSkI4wZ97WObbW7khDmGv4jiNpnZVxhl4Rjlw4peSwdfmFoGh6aaGvPeXWs'
