from flask import render_template
from flask_rest_api import Api


class MyApi(Api):
    def _openapi_swagger_ui(self):
        return render_template('swaggerui.html', title=self._app.name)


def register_blueprints(app, prefix, blueprints):
    for blueprint in blueprints:
        app.api.register_blueprint(
            blueprint,
            url_prefix='{}/{}'.format(
                prefix,
                blueprint.name,
            ),
        )


def create_api(app):
    from .auth import blueprint as auth
    from .application import blueprint as application
    from .cluster import blueprint as cluster
    from .host import blueprint as host
    from .me import blueprint as me
    from .provider import blueprint as provider
    from .service import blueprint as service
    from .user import blueprint as user

    app.api = MyApi(app)
    register_blueprints(
        app,
        '/api/v0',
        [
            auth,
            cluster,
            me,
            provider,
            service,
            user,
        ],
    )
