#!/usr/bin/env python
from flask.ext.security.registerable import register_user
from onelove import OneLove

from manage import onelove
from onelove.models import User


ctx = onelove.app.test_request_context().push()

# Create admin user
try:
    user = User.objects.get(email='admin@example.com')
except User.DoesNotExist:
    user = register_user(email='admin@example.com', password='Sekrit')

# Create admin role
admin_role = OneLove.user_datastore.find_or_create_role(
    name="admin",
    description="Administrator"
)

# Add admin user to admin role
OneLove.user_datastore.add_role_to_user(user, admin_role)
