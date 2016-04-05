from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Task',
    {
        'celery_id': String(),
        'error_message': String(),
        'status': String(),
    },
)
