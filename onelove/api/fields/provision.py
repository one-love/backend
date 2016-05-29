from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Provision',
    {
        'id': String(),
        'status': String(),
    },
)
