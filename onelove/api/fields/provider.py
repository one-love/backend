from flask_restplus.fields import String
from .. import api


put_fields = api.model(
    'Put Provider',
    {
        'name': String(required=True),
    },
)

fields = api.clone(
    'Provider',
    put_fields,
    {
        'type': String(required=True),
    },
)
