#!/usr/bin/env python
from flask_security.utils import encrypt_password

from manage import onelove
from onelove.models import User


ctx = onelove.app.test_request_context().push()

# Create admin user
try:
    user = User.objects.get(email='admin@example.com')
except User.DoesNotExist:
    user = User(email='admin@example.com')
    user.password = encrypt_password('Sekrit')
    user.username = 'admin'
    user.active = True
    user.save()

# Create admin role
admin_role = onelove.user_datastore.find_or_create_role(
    name="admin",
    description="Administrator"
)

# Add admin user to admin role
onelove.user_datastore.add_role_to_user(user, admin_role)
