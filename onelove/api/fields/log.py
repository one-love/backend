from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Log',
    {
        'status': String(),
        'host': String(),
        'task': String(),
        'timestamp': String(),
        'log': String(),
    },
)
