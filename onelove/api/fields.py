from flask.ext.restplus import fields
from . import api

# User fields
user_fields = api.model(
    'User', {
        'email': fields.String(
            description='The email',
            required=True,
            default='admin@example.com'
        ),
        'first_name': fields.String,
        'last_name': fields.String,
        'password': fields.String(
            description='Password',
            required=True,
            default='Sekrit'
        ),
    }
)

get_user_fields = api.extend(
    'Get Users', user_fields, {
        'id': fields.String,
    }
)

# Auth fields
auth_fields = api.model(
    'Auth', {
        'email': fields.String(description='The email', required=True, default='admin@example.com'),
        'password': fields.String(description='The password', required=True, default='Sekrit'),
    }
)

token_response = api.model(
    'Token', {
        'token': fields.String,
    }
)

# Application fields
application_fields = api.model(
    'Application', {
        'application_name': fields.String(required=True),
        'galaxy_role': fields.String(required=True),
        'name': fields.String(required=True),
    }
)

# Provider fields
provider_fields = api.model(
    'Provider', {
        'name': fields.String(required=True),
        'type': fields.String(required=True),
    }
)

# Cluster fields
cluster_fields = api.model(
    'Cluster', {
        'applications': fields.Nested(application_fields),
        'name': fields.String(required=True),
        'providers': fields.Nested(provider_fields),
    }
)

get_cluster_fields = api.extend('Get Clusters', cluster_fields, {
        'id': fields.String,
    }
)

# Task fields
task_fields = api.model(
    'Task', {
    'id': fields.String,
    'celery_id': fields.String,
    }
)
