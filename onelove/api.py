from django.contrib.auth import get_user_model
from tastypie.authorization import Authorization
from tastypie_mongoengine import resources, fields

from .models import Fleet, Application, Provider


class UserResource(resources.MongoEngineResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'user'
        excludes = ['password']


class ApplicationResource(resources.MongoEngineResource):
    class Meta:
        object_class = Application


class ProviderResource(resources.MongoEngineResource):
    class Meta:
        object_class = Provider


class FleetResource(resources.MongoEngineResource):
    applications = fields.EmbeddedListField(
        of='onelove.api.ApplicationResource',
        attribute='applications',
        full=True,
        null=True
    )

    providers = fields.EmbeddedListField(
        of='onelove.api.ProviderResource',
        attribute='providers',
        full=True,
        null=True
    )

    class Meta:
        queryset = Fleet.objects.all()
        authorization = Authorization()
