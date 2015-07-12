#!/usr/bin/env python
from flask import redirect, url_for

from init import manager
from app import celery


@manager.app.route('/')
def index():
    return redirect(url_for('servers'))


if __name__ == '__main__':
    manager.run()
