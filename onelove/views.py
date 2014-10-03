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
        queryset = self.serializer_class.Meta.model.objects.filter(
            group__in=self.request.user.groups.all()
        )
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def pre_save(self, obj):
        """
        Handle user password
        """
        if 'password' in self.request._data:
            obj.set_password(obj.password)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = serializer_class.Meta.model.objects.all()
