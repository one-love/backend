from rest_framework import serializers
from fleets.models import Fleet, Application, AmazonProvider


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = (
            'id',
            'name',
            'url',
        )


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'name',
            'repo',
            'fleet',
        )


class AmazonProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonProvider
        fields = (
            'id',
            'name',
            'access_key',
            'security_key',
            'fleet',
        )
