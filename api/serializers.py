from rest_framework_mongoengine import serializers
from fleets.models import Fleet, Application, Provider


class FleetSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Fleet


class ApplicationSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Application


class ProviderSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Provider
