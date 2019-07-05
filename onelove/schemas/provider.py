from marshmallow import fields

from .base import BaseSchema


class ProviderSchema(BaseSchema):
    id = fields.String(description='ID', dump_only=True)
    name = fields.String(required=True, description='name')
    type = fields.String(required=True, description='type')
