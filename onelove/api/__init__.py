from flask import Blueprint, render_template
from flask.ext.restplus import Api


api_v0 = Blueprint('api', __name__)

api = Api(
    api_v0,
    version='0',
    title='OneLove API',
    description='API for OneLove project.',
    ui=False
)


@api_v0.route('/doc/', endpoint='doc')
def swagger_ui():
    return render_template(
        'flask-restplus/swagger-ui.html',
        title=api.title,
        specs_url=api.specs_url
    )


from . import auth
from . import user
