from marshmallow import fields

from .base import BaseSchema


class ApplicationSchema(BaseSchema):
    name = fields.String(description='Application name', required=True)
    galaxy_role = fields.String(description='Galaxy role', required=True)
