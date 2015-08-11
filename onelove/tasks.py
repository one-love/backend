from celery import current_app


@current_app.task
def add(x, y):
    return x + y


@current_app.task
def provision(app):
    return app
