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

    def get_queryset(self):
        user = self.request.user
        groups = user.groups.all()
        queryset = self.serializer_class.Meta.model.objects.filter(
            group__in=groups
        )
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializer_class.Meta.model.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = serializer_class.Meta.model.objects.all()
