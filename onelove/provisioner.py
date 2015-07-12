from celery import Celery


celery = Celery('onelove')


@celery.task
def add(x, y):
    return x + y


@celery.task
def current_path():
    import os
    return os.path.curdir
