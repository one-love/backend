from rest_framework import serializers
from .. import models


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = ('id', 'name', 'repo', 'fleet')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = ('id', 'name', 'access_key', 'security_key', 'fleet')


class FleetSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True)
    providers = ProviderSerializer(many=True)

    class Meta:
        model = models.Fleet
        fields = ('id', 'name', 'url', 'user', 'applications', 'providers')
