from celery import Celery

celery = Celery('tasks', backend='rpc://', broker='amqp://guest@172.17.0.6//')


@celery.task
def add(x, y):
    return x + y


@celery.task
def current_path():
    import os
    return os.path.curdir
