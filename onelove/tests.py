from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import json


class APITest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        data = {
            'username': 'admin@example.com',
            'password': 'Sekrit',
        }
        response = cls.client.post(
            path=reverse('login'),
            data=data,
        )
        cls.token = json.loads(response.content)['token']

    def test_v1_dummy(self):
        self.assertEqual(200, 200)
