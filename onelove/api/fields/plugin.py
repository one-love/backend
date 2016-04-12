from flask_restplus.fields import String, Nested
from .. import api


properties_fields = api.model(
    'Properties',
    {
        'name': String(required=True),
        'type': String(required=True),
    },
)


provider_fields = api.model(
    'Providers',
    {
        'type': String(required=True),
        'properties': Nested(properties_fields),
    },
)
