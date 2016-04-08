from flask_restplus.fields import String
from .. import api


provider_fields = api.model(
    'Providers', {
        'type': String(required=True),
    }
)
