from celery import current_app


@current_app.task
def add(x, y):
    return x + y


@current_app.task
def current_path():
    import os
    return os.path.curdir
