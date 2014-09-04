from tastypie_mongoengine import resources
from .models import Fleet


class FleetResource(resources.MongoEngineResource):
    class Meta:
        queryset = Fleet.objects.all()
