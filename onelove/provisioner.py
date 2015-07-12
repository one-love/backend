from celery import Celery
from config import BaseConfig

celery = Celery('onelove')


@celery.task
def add(x, y):
    return x + y


@celery.task
def current_path():
    import os
    return os.path.curdir
