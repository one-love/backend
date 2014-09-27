from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from .models import User


class APITest(APITestCase):
    def setUp(self):
        """
        Setup token
        """
        user = User.objects.get(email='admin@example.com')
        self.token, created = Token.objects.get_or_create(user=user)

    def test_v1_get_fleet(self):
        """
        Simple GET on ''fleet-list' URL with anonymous and authenticated user
        """
        endpoint = 'fleet-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
