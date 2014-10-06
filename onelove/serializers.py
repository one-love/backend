from django.contrib.auth.models import Group
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
    class Meta:
        model = models.User
        write_only_fields = ('password',)
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'groups',
            'user_permissions',
        )


class GroupSerializer(serializers.ModelSerializer):
    fleets = FleetSerializer(many=True, read_only=True)

    class Meta:
        model = Group


class SSHProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SSHProvider


class AWSProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AWSProvider


class SSHHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SSHHost
