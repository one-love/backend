from rest_framework import viewsets
from . import serializers


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProviderSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ApplicationSerializer
    queryset = serializer_class.Meta.model.objects.all()


class FleetViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FleetSerializer
    queryset = serializer_class.Meta.model.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
