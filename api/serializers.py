from rest_framework import serializers
from fleets.models import Fleet, Application, AmazonProvider


class FleetSerializer(serializers.ModelSerializer):
    applications = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    amazon_providers = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Fleet
        fields = (
            'id',
            'name',
            'url',
            'applications',
            'amazon_providers',
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
