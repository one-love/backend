from rest_framework import viewsets
from rest_framework import generics


from . import serializers
from fleets.models import Fleet, Application, Provider


class FleetList(generics.ListCreateAPIView):
    model = Fleet
    serializer_class = serializers.FleetSerializer

    def get_queryset(self):
        return Fleet.objects


class FleetDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Fleet
    serializer_class = serializers.FleetSerializer


class FleetViewSet(viewsets.ModelViewSet):
    model = Fleet
    serializer_class = serializers.FleetSerializer

    def pre_save(self, obj):
        obj.user = self.request.user


class ApplicationViewSet(viewsets.ModelViewSet):
    model = Application
    serializer_class = serializers.ApplicationSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    model = Provider
    serializer_class = serializers.ProviderSerializer
