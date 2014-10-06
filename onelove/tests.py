from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from . import models, factories
from django.test import TestCase


class ModelTest(TestCase):
    def test_application(self):
        fleet = factories.FleetFactory()
        application = models.Application(
            name='app',
            repo='https://github.com/one-love/ansible-one-love',
            fleet=fleet,
        )
        application.save()
        get_application = models.Application.objects.get(
            name=application.name
        )
        self.assertEqual(application, get_application)

    def test_awsprovider(self):
        fleet = factories.FleetFactory()
        provider = models.AWSProvider(
            name='awsprovider',
            fleet=fleet,
            type='awsprovider',
        )
        provider.save()
        get_provider = models.Provider.objects.get_subclass(name=provider.name)
        self.assertEqual(provider, get_provider)

    def test_fleet(self):
        group = factories.GroupFactory()
        fleet = models.Fleet(
            name='fleet',
            url='https://www.google.com/',
            group=group,
        )
        fleet.save()
        get_fleet = models.Fleet.objects.get(name=fleet.name)
        self.assertEqual(fleet, get_fleet)

    def test_sshhost(self):
        ssh_provider = factories.SSHProviderFactory()
        ssh_host = models.SSHHost(
            ip='192.168.192.168',
            ssh_provider=ssh_provider,
        )
        ssh_host.save()
        get_sshhost = models.SSHHost.objects.get(pk=ssh_host.pk)
        self.assertEqual(ssh_host, get_sshhost)

    def test_sshprovider(self):
        fleet = factories.FleetFactory()
        provider = models.AWSProvider(
            name='sshprovider',
            fleet=fleet,
            type='sshprovider',
        )
        provider.save()
        get_provider = models.Provider.objects.get_subclass(name=provider.name)
        self.assertEqual(provider, get_provider)

    def test_user(self):
        user = models.User(
            email='one@love.com',
        )
        user.save()
        get_user = models.User.objects.get(email=user.email)
        self.assertEqual(user, get_user)

    def test_user_manager(self):
        user = models.User.objects.create(email='one@love.com')
        user.save()
        self.assertEqual(user.email, 'one@love.com')


class FactoriesTest(TestCase):
    def test_appliction(self):
        application = factories.ApplicationFactory()
        get_application = models.Application.objects.get(
            name=application.name
        )
        self.assertEqual(application, get_application)

    def test_awsprovider(self):
        provider = factories.AWSProviderFactory()
        get_provider = models.Provider.objects.get_subclass(
            name=provider.name
        )
        self.assertEqual(provider, get_provider)

    def test_fleet(self):
        fleet = factories.FleetFactory()
        get_fleet = models.Fleet.objects.get(name=fleet.name)
        self.assertEqual(fleet, get_fleet)

    def test_sshhost(self):
        host = factories.SSHHostFactory()
        get_host = models.SSHHost.objects.get(ip=host.ip)
        self.assertEqual(host, get_host)

    def test_sshprovider(self):
        provider = factories.SSHProviderFactory()
        get_provider = models.Provider.objects.get_subclass(
            name=provider.name
        )
        self.assertEqual(provider, get_provider)

    def test_user(self):
        user = models.User(email='some@onelove.com')
        user.save()
        get_user = models.User.objects.get(email='some@onelove.com')
        self.assertEqual(user, get_user)


class APIv1Test(APITestCase):
    def setUp(self):
        """
        Setup token
        """
        user = models.User.objects.get(email='admin@example.com')
        self.token, created = Token.objects.get_or_create(user=user)

    def test_get_applications(self):
        endpoint = 'application-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_fleets(self):
        endpoint = 'fleet-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_groups(self):
        endpoint = 'group-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_providers(self):
        endpoint = 'provider-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_providers_hosts(self):
        endpoint = 'provider-hosts'
        ssh_host = factories.SSHHostFactory()
        args = (ssh_host.ssh_provider.pk,)
        response = self.client.get(path=reverse(endpoint, args=args))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint, args=args))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        endpoint = 'user-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_applications(self):
        endpoint = 'application-list'
        fleet = factories.FleetFactory()
        data = {
            'name': u'application',
            'repo': u'https://github.com/one-love/wordpress.git',
            'playbook': u'provision/site.yml',
            'fleet': fleet.id,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        self.assertEqual(dict(response.data), data)

    def test_post_fleets(self):
        endpoint = 'fleet-list'
        group = factories.GroupFactory()
        data = {
            'name': u'fleet',
            'url': u'http://onelove.org/',
            'group': group.pk,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['applications'] = []
        data['id'] = response.data['id']
        data['providers'] = []
        self.assertEqual(dict(response.data), data)

    def test_post_groups(self):
        endpoint = 'group-list'
        data = {
            'name': u'group',
            'permissions': [],
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        data['fleets'] = []
        self.assertEqual(dict(response.data), data)

    def test_post_providers(self):
        endpoint = 'provider-list'
        fleet = factories.FleetFactory()
        data = {
            'name': u'aws',
            'type': u'awsprovider',
            'access_key': u'sdfvsdvdsf',
            'security_key': u'vsdfvdsfgrvvfsdfvd',
            'ssh_key': u'dsvdsvfd',
            'fleet': fleet.id,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['id'] = response.data['id']
        self.assertEqual(dict(response.data), data)

        data = {
            'name': u'ssh',
            'type': u'sshprovider',
            'ssh_key': u'dsvdsvfd',
            'fleet': fleet.id,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['id'] = response.data['id']
        self.assertEqual(dict(response.data), data)

    def test_post_providers_hosts(self):
        endpoint = 'provider-hosts'
        ssh_host = factories.SSHHostFactory()
        args = (ssh_host.ssh_provider.pk,)
        data = {
            'ip': u'192.168.1.11'
        }
        response = self.client.post(
            path=reverse(endpoint, args=args),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint, args=args),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        data['ssh_provider'] = ssh_host.ssh_provider.pk
        self.assertEqual(dict(response.data), data)

    def test_post_users(self):
        endpoint = 'user-list'
        data = {
            'email': u'some@example.com',
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        data['first_name'] = response.data['first_name']
        data['last_name'] = response.data['last_name']
        data['groups'] = response.data['groups']
        data['is_active'] = response.data['is_active']
        data['user_permissions'] = response.data['user_permissions']
        self.assertEqual(dict(response.data), data)
