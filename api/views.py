from rest_framework import viewsets

from . import serializers
from fleets.models import Fleet, Application, AmazonProvider


class FleetViewSet(viewsets.ModelViewSet):
    model = Fleet
    serializer_class = serializers.FleetSerializer

    def get_queryset(self):
        user = self.request.user
        return Fleet.objects.filter(user=user)

    def pre_save(self, obj):
        obj.user = self.request.user


class ApplicationViewSet(viewsets.ModelViewSet):
    model = Application
    serializer_class = serializers.ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        fleets = Fleet.objects.filter(user=user)
        fleet_ids = [f.id for f in fleets]
        return self.model.objects.filter(fleet__in=fleet_ids)


class AmazonProviderViewSet(viewsets.ModelViewSet):
    model = AmazonProvider
    serializer_class = serializers.AmazonProviderSerializer

    def get_queryset(self):
        user = self.request.user
        fleets = Fleet.objects.filter(user=user)
        fleet_ids = [f.id for f in fleets]
        return self.model.objects.filter(fleet__in=fleet_ids)
