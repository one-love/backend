from marshmallow import fields

from .base import BaseSchema


class ClusterSchema(BaseSchema):
    id = fields.String(description='ID', dump_only=True)
    name = fields.String(required=True, description='name')
