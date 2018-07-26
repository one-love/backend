from flask import Blueprint, render_template
from flask_jwt import JWTError
from flask_restplus import Api, apidoc


api = None


def create_api(app):
    """ Create blueprints for API and Doc and register them in app """
    global api
    blueprint = Blueprint('api', __name__)
    api = Api(
        blueprint,
        version='0',
        title='AWS Cognito Wrapper API',
        description='Api that exposes endpoints for AWS Cognito',
        catch_all_404s=False,
        doc='/api/v0/doc/',
        default='auth',
    )
    app.api = api
    app.register_blueprint(blueprint)
    app.register_blueprint(apidoc.apidoc)

    import onelove.api.application
    import onelove.api.auth
    import onelove.api.cluster
    import onelove.api.cluster_services
    import onelove.api.host
    import onelove.api.me
    import onelove.api.plugin
    import onelove.api.provider
    import onelove.api.provision
    import onelove.api.service
    import onelove.api.service_provision
    import onelove.api.user
