from unittest import TestCase


from onelove import OneLove
from onelove.utils import create_app


class TestAPI(TestCase):
    def setUp(self):
        self.onelove = OneLove(create_app(config_name='testing'))
        self.app = self.onelove.app.test_client()
        self.token = self.login('admin@example.com', 'Sekrit')

    def login(self, email, password):
        import json
        response = self.app.post(
            '/api/v0/auth/tokens',
            data=json.dumps({'email': email, 'password': password}),
            content_type='application/json',
            follow_redirects=True,
        )
        json_response = json.loads(response.data)
        return json_response['token']

    def get(self, url):
        response = self.app.get(
            url,
            headers={
                'Authorization': 'JWT {token}'.format(token=self.token)
            },
        )
        return response

    def test_default_admin_login(self):
        self.assertEqual(len(self.token), 201)

    def test_empty_clusters(self):
        response = self.get('/api/v0/clusters')
        self.assertLess(response.status_code, 400)
