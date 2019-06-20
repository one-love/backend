from marshmallow import fields

from .application import ApplicationSchema
from .auth import UserSchema
from .base import BaseSchema


class ServiceSchema(BaseSchema):
    id = fields.String(description='ID', dump_only=True)
    name = fields.String(required=True, description='Service name')
    applications = fields.Nested(ApplicationSchema, dump_only=True, many=True)
    user = fields.Nested(UserSchema, dump_only=True)
