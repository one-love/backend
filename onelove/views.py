from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from . import serializers, tasks
from .models import Provider


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProviderSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @detail_route(methods=['GET', 'POST'])
    def hosts(self, request, pk):
        if request.method == 'POST':
            provider = Provider.objects.get_subclass(pk=pk)
            if provider.type != 'sshprovider':
                raise ParseError(
                    detail="Only SSH Provider has ability to add hosts by hand"
                )
            data = request.DATA
            data['ssh_provider'] = pk
            serializer = serializers.SSHHostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            provider = Provider.objects.get_subclass(pk=pk)
        except Provider.DoesNotExist:
            raise Http404

        return Response(
            {
                'hosts': [host.ip for host in provider.get_hosts()]
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        if 'type' not in request.DATA:
            raise ParseError(
                detail="'type' must be 'awsprovider' or 'sshprovider'"
            )
        elif request.DATA['type'] == 'awsprovider':
            serializer = serializers.AWSProviderSerializer(data=request.DATA)
        elif request.DATA['type'] == 'sshprovider':
            serializer = serializers.SSHProviderSerializer(data=request.DATA)
        else:
            raise ParseError(
                detail="'type' must be 'awsprovider' or 'sshprovider'"
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    @detail_route(methods=['POST'])
    def provision(self, request, pk):
        config = {
            'repo': 'https://github.com/one-love/ansible-wordpress',
            'inventory': 'provision/vagrant',
            'playbook': 'provision/site.yml',
            'remote_pass': 'vagrant',
        }
        result = tasks.provision.delay(config)

        return Response(
            {
                'result': result.id
            },
            status=status.HTTP_201_CREATED,
        )


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
