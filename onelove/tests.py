from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class APITest(TestCase):
    def test_v1_authentication(self):
        client = Client()
        data = {
            'username': 'admin@example.com',
            'password': 'Sekrit',
        }
        response = client.post(
            path=reverse('login'),
            data=data,
        )
        self.assertEqual(response.status_code, 200)
