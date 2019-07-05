from marshmallow import fields

from .base import BaseSchema


class HostSSHSchema(BaseSchema):
    id = fields.String(description='ID', dump_only=True)
    hostname = fields.String(required=True, description='hostname')
    ip = fields.String(required=True, description='IP Address')
    tags = fields.List(fields.String(), description='Host tags')
