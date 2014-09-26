from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class APITest(TestCase):
    def test_v1_application_endpoint(self):
        client = Client()
        response = client.get(reverse('api:v1:application-list'))
        self.assertEqual(response.status_code, 200)
