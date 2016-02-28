from unittest import TestCase

import json


class TestAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        from onelove import OneLove
        from onelove.utils import create_app
        app = create_app(config_name='testing')
        cls.onelove = OneLove(app)
        cls.onelove.app.test_request_context().push()
        cls.app = cls.onelove.app.test_client()

        from onelove import factories
        cls.me = factories.UserFactory.create()

        admin_role = cls.onelove.user_datastore.find_or_create_role(
            name="admin",
            description="Administrator"
        )
        cls.onelove.user_datastore.add_role_to_user(cls.me, admin_role)
        cls.token = cls.login(cls.me.email, 'Sekrit')

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

    def post(self, url, data):
        response = self.app.post(
            url,
            data=json.dumps(data),
            headers={
                'Authorization': 'JWT {token}'.format(token=self.token),
                'Content-Type': 'application/json',
            },
        )
        self.assertLess(response.status_code, 400)
        return json.loads(response.data)

    def put(self, url, data):
        response = self.app.put(
            url,
            data=json.dumps(data),
            headers={
                'Authorization': 'JWT {token}'.format(token=self.token),
                'Content-Type': 'application/json',
            },
        )
        print(response)
        self.assertLess(response.status_code, 400)
        return json.loads(response.data)

    def delete(self, url):
        response = self.app.delete(
            url,
            headers={
                'Authorization': 'JWT {token}'.format(token=self.token)
            },
        )
        self.assertLess(response.status_code, 400)
        return json.loads(response.data)

    def test_cluster(self):
        from onelove.models import Cluster, Role
        url_list = '/api/v0/clusters'
        data = {'name': 'first'}

        response = self.get(url=url_list)
        self.assertEqual(response, [])

        response = self.post(url=url_list, data=data)
        self.assertEqual(data['name'], response['name'])

        url_detail = '/api/v0/clusters/{pk}'.format(pk=response['id'])
        response = self.get(url=url_detail)
        cluster = Cluster(response['name'])
        roles = [
            {
                u'admin': u'True',
                u'name': u'admin_{name}'.format(name=data['name']),
                u'description': u'Cluster {name} admin'.format(name=data['name']),
            },
            {
                u'admin': u'False',
                u'name': u'user_{name}'.format(name=data['name']),
                u'description': u'Cluster {name} users'.format(name=data['name']),
            },
        ]
        self.assertEqual(roles, response['roles'])
        self.assertEqual(cluster.name, response['name'])
        self.assertEqual(cluster.applications, response['applications'])
        self.assertEqual(cluster.providers, response['providers'])

        data = {'name': 'second'}
        response = self.put(url=url_detail, data=data)
        cluster = Cluster(response['name'])
        self.assertEqual(cluster.name, response['name'])

        response = self.delete(url=url_detail)
        self.assertEqual(data, response)
        for item in roles:
            role = Role.objects(name=item['name'])
            role.delete()

    def test_me(self):
        from onelove.models import User
        url = '/api/v0/me'
        data = self.get(url)
        del data['id']
        api_user = User(data)
        api_user.pk = self.me.pk
        self.assertEqual(self.me, api_user)
