from flask_restplus.fields import String, Nested
from .. import api
from .host import fields as host_fields

patch_fields = api.model(
    'Patch provider',
    {
        'name': String(required=True),
    },
)

fields = api.clone(
    'Provider',
    patch_fields,
    {
        'type': String(required=True),
        'hosts': Nested(host_fields),
    },
)
