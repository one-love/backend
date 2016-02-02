from unittest import TestCase

from onelove import OneLove
from onelove.utils import create_app
import json


class TestAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.onelove = OneLove(create_app(config_name='testing'))
        cls.onelove.app.test_request_context().push()
        cls.app = cls.onelove.app.test_client()

        from onelove.models import User
        from flask_security.utils import encrypt_password
        cls.me = User(email='admin@example.com')
        cls.me.password = encrypt_password('Sekrit')
        cls.me.save()

        admin_role = cls.onelove.user_datastore.find_or_create_role(
            name="admin",
            description="Administrator"
        )
        cls.onelove.user_datastore.add_role_to_user(cls.me, admin_role)
        cls.token = cls.login('admin@example.com', 'Sekrit')

    @classmethod
    def tearDownClass(cls):
        cls.onelove.db.connection.drop_database('test')

    @classmethod
    def login(cls, email, password):
        import json
        response = cls.app.post(
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
        self.assertLess(response.status_code, 400)
        data = json.loads(response.data)
        return data

    def test_default_admin_login(self):
        self.assertEqual(len(self.token), 201)

    def test_empty_clusters(self):
        data = self.get('/api/v0/clusters')
        self.assertEqual([], data)

    def test_clusters(self):
        from onelove.models import Cluster
        cluster = Cluster(name='name')
        cluster.save()
        url = '/api/v0/clusters/{id}'.format(id=str(cluster.id))
        data = self.get(url)
        self.assertEqual(str(cluster.id), data['id'])
        self.assertEqual(cluster.name, data['name'])
        self.assertEqual(cluster.applications, data['applications'])
        self.assertEqual(cluster.providers, data['providers'])
        self.assertEqual(cluster.roles, data['roles'])
        cluster.delete()

    def test_me(self):
        url = '/api/v0/me'
        data = self.get(url)
        self.assertEqual(str(self.me.id), data['id'])
        self.assertEqual(self.me.email, data['email'])
        self.assertEqual(self.me.first_name, data['first_name'])
        self.assertEqual(self.me.last_name, data['last_name'])
        for role in data['roles']:
            self.assertTrue(self.me.has_role(role['name']))
        self.assertEqual(len(self.me.roles), len(data['roles']))
