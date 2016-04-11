from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Task',
    {
        'id': String(),
        'status': String(),
    },
)
