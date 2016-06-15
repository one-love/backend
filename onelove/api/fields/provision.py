from flask_restplus.fields import String, Nested
from .. import api
from .log import fields as log_fields


fields = api.model(
    'Provision',
    {
        'id': String(),
        'status': String(),
        'logs': Nested(log_fields),
    },
)
