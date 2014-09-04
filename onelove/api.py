from django.contrib.auth import get_user_model
from tastypie.authorization import Authorization
from tastypie_mongoengine import resources
from mongoengine import fields

from .models import Fleet, Application


class UserResource(resources.MongoEngineResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'user'
        excludes = ['password']


class FleetResource(resources.MongoEngineResource):
    class Meta:
        queryset = Fleet.objects.all()
        authorization = Authorization()
