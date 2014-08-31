from rest_framework import serializers
from fleets.models import Fleet


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = (
            'id',
            'name',
            'url',
        )
