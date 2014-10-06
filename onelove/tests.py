from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from . import models, factories
from django.contrib.auth.models import Group
from django.test import TestCase


class ModelTest(TestCase):
    def test_appliction(self):
        """
        Test creating Application
        """
        application = factories.ApplicationFactory()
        get_application = models.Application.objects.get(
            name=application.name
        )
        self.assertEqual(application, get_application)

    def test_awsprovider(self):
        """
        Test creating AWSProvider
        """
        provider = factories.AWSProviderFactory()
        get_provider = models.Provider.objects.get_subclass(
            name=provider.name
        )
        self.assertEqual(provider, get_provider)

    def test_fleet(self):
        """
        Test creating Fleet
        """
        fleet = factories.FleetFactory()
        get_fleet = models.Fleet.objects.get(name=fleet.name)
        self.assertEqual(fleet, get_fleet)

    def test_sshhost(self):
        """
        Test creating SSHHost

        """
        host = factories.SSHHostFactory()
        get_host = models.SSHHost.objects.get(ip=host.ip)
        self.assertEqual(host, get_host)

    def test_sshprovider(self):
        """
        Test creating SSHProvider
        """
        provider = factories.SSHProviderFactory()
        get_provider = models.Provider.objects.get_subclass(
            name=provider.name
        )
        self.assertEqual(provider, get_provider)

    def test_users(self):
        """
        Test creating User
        """
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

    def test_get_fleets(self):
        """
        GET on 'fleet-list' URL with anonymous and authenticated user
        """
        endpoint = 'fleet-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_groups(self):
        """
        GET on 'group-list' URL with anonymous and authenticated user
        """
        endpoint = 'group-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        """
        GET on 'user-list' URL with anonymous and authenticated user
        """
        endpoint = 'user-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_applications(self):
        """
        GET on 'application-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'application-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_providers(self):
        """
        GET on 'provider-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'provider-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_groups(self):
        """
        POST on 'group-list' URL with anonymous and authenticated user
        """
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

    def test_post_users(self):
        """
        POST on 'user-list' URL with anonymous and authenticated user
        """
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

    def test_post_fleets(self):
        """
        POST on 'fleet-list' URL with anonymous and authenticated user
        """
        endpoint = 'fleet-list'
        group = Group.objects.create(name='wordpress')
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

    def test_post_applications(self):
        """
        POST on 'application-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'application-list'
        group = Group.objects.create(name='wordpress')
        fleet = models.Fleet.objects.create(group=group)
        data = {
            'name': u'application',
            'repo': u'https://github.com/one-love/wordpress.git',
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

    def test_post_providers(self):
        """
        POST on 'provider-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'provider-list'
        group = Group.objects.create(name='wordpress')
        fleet = models.Fleet.objects.create(group=group)
        data = {
            'name': u'aws',
            'type': u'awsprovider',
            'access_key': u'sdfvsdvdsf',
            'security_key': u'vsdfvdsfgrvvfsdfvd',
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
