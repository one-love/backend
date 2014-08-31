from rest_framework import viewsets

from . import serializers
from fleets.models import Fleet


class FleetViewSet(viewsets.ModelViewSet):
    queryset = Fleet.objects.all()
    serializer_class = serializers.FleetSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
