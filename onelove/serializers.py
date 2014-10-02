from rest_framework import serializers
from . import models


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = ('id', 'name', 'repo', 'fleet')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider


class FleetSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True, read_only=True)
    providers = ProviderSerializer(many=True, read_only=True)

    class Meta:
        model = models.Fleet


class UserSerializer(serializers.ModelSerializer):
    fleets = FleetSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
