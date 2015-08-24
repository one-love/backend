#!/usr/bin/env python
from flask.ext.security.registerable import register_user

from manage import onelove
from onelove.models import User


ctx = onelove.app.test_request_context()
ctx.push()
try:
    user = User.objects.get(email='admin@example.com')
except User.DoesNotExist:
    user = register_user(email='admin@example.com', password='Sekrit')
