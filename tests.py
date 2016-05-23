from unittest import TestCase
from base64 import b64encode, b64decode

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
        self.assertLess(response.status_code, 400)
        return json.loads(response.data)

    def patch(self, url, data):
        response = self.app.patch(
            url,
            data=json.dumps(data),
            headers={
                'Authorization': 'JWT {token}'.format(token=self.token),
                'Content-Type': 'application/json',
            },
        )
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

        # Prepare
        url_list = '/api/v0/clusters'
        data = {
            'name': 'first',
            'username': 'vagrant',
            'sshKey': b64encode('fake key'),
        }

        # Get empty list
        response = self.get(url=url_list)
        self.assertEqual(response, [])

        # Create item
        response = self.post(url=url_list, data=data)
        self.assertEqual(data['name'], response['name'])
        self.assertEqual(data['username'], response['username'])

        # Get item details
        url_detail = '/api/v0/clusters/{pk}'.format(pk=response['id'])
        response = self.get(url=url_detail)
        cluster = Cluster.objects.get(name=response['name'])
        roles = [
            {
                u'admin': u'True',
                u'name': u'admin_{name}'.format(name=data['name']),
                u'description': u'Cluster {name} admin'.format(
                    name=data['name']
                ),
            },
            {
                u'admin': u'False',
                u'name': u'user_{name}'.format(name=data['name']),
                u'description': u'Cluster {name} users'.format(
                    name=data['name']
                ),
            },
        ]
        self.assertEqual(roles, response['roles'])
        self.assertEqual(cluster.name, response['name'])
        self.assertEqual(cluster.username, response['username'])
        self.assertEqual(cluster.services, response['services'])
        self.assertEqual(cluster.providers, response['providers'])

        # Change item details
        data = {
            'name': 'second',
            'username': 'vagrant',
            'sshKey': b64encode('another fake'),
        }
        response = self.put(url=url_detail, data=data)
        cluster = Cluster.objects.get(name=response['name'])
        self.assertEqual(cluster.name, response['name'])
        self.assertEqual(cluster.username, response['username'])

        # Change item details
        data = {
            'name': 'third',
        }
        response = self.patch(url=url_detail, data=data)
        cluster = Cluster.objects.get(name=response['name'])
        self.assertEqual(cluster.name, response['name'])
        self.assertEqual(cluster.username, response['username'])

        data = {
            'username': 'example'
        }
        response = self.patch(url=url_detail, data=data)
        cluster = Cluster.objects.get(name=response['name'])
        self.assertEqual(cluster.name, response['name'])
        self.assertEqual(cluster.username, response['username'])

        data = {
            'sshKey': b64encode('example fake'),
        }
        response = self.patch(url=url_detail, data=data)
        cluster = Cluster.objects.get(name=response['name'])
        self.assertEqual(cluster.name, response['name'])
        self.assertEqual(cluster.username, response['username'])

        # Delete item
        data = {
            'name': 'third',
            'username': 'example',
            'sshKey': b64encode('example fake'),
        }
        response = self.delete(url=url_detail)
        self.assertEqual(data['name'], response['name'])
        self.assertEqual(data['username'], response['username'])

        # Cleanup
        for item in roles:
            role = Role.objects(name=item['name'])
            role.delete()

        for service in cluster.services:
            service.delete()

        cluster.delete

    def test_cluster_service(self):
        from onelove import factories
        from onelove.models import Cluster

        # Prepare
        cluster = factories.ClusterFactory.create()
        cluster.save()
        service = factories.ServiceFactory.create(user=self.me)
        service.save()
        url_list='/api/v0/clusters/{pk}/services'.format(pk=cluster.pk)
        data={
            'service_id': str(service.pk),
        }

        # Get empty list
        response = self.get(url=url_list)
        self.assertEqual(response, [])

        # Create item
        response = self.post(url=url_list, data=data)
        self.assertEqual(data['service_id'], response['id'])

        # Delete item
        url_detail = '/api/v0/clusters/{pk}/services/{ps}'.format(pk=cluster.pk, ps=response['id'])
        response = self.delete(url=url_detail)
        self.assertEqual(data['service_id'],response['id'])

        cluster.delete()
        service.delete()

    def test_me(self):
        from onelove.models import User
        url = '/api/v0/me'
        data = self.get(url)
        del data['id']
        api_user = User(data)
        api_user.pk = self.me.pk
        self.assertEqual(self.me, api_user)

    def test_service(self):
        from onelove.models import Service

        for service in Service.objects.all():
            service.delete()

        # Prepare
        url_list = '/api/v0/services'
        data = {
            'name': 'first'
        }
        # Get empty list
        response = self.get(url=url_list)
        self.assertEqual(response, [])

        # Create item
        response = self.post(url=url_list, data=data)
        self.assertEqual(data['name'], response['name'])

        # Get item details
        url_detail='/api/v0/services/{pk}'.format(pk=response['id'])
        response = self.get(url=url_detail)
        service = Service.objects.get(name=response['name'])
        self.assertEqual(service.name, response['name'])

        # Change item details
        data = {
            'name': 'second'
        }
        response = self.put(url=url_detail, data=data)
        service = Service.objects.get(name=response['name'])
        self.assertEqual(service.name, response['name'])

        # Change item details
        data = {
            'name': 'third',
        }
        response = self.patch(url=url_detail, data=data)
        service = Service.objects.get(name=response['name'])
        self.assertEqual(service.name, response['name'])

        # Delete item
        response = self.delete(url=url_detail)
        self.assertEqual(data['name'], response['name'])

    def test_service_applications(self):
        from onelove.models import Service
        from onelove import factories

        for service in Service.objects.all():
            service.delete()

        # Prepare
        service = factories.ServiceFactory.create(
            user=self.me,
            applications=[],
        )
        service.save()
        url_list = '/api/v0/services/{pk}/applications'.format(
            pk=str(service.pk)
        )
        data = {
            'galaxy_role': 'super',
            'name': 'first'
        }

        # Get empty list
        response = self.get(url_list)
        self.assertEqual(response,[])

        # Create item
        response = self.post(url=url_list, data=data)
        self.assertEqual(data['galaxy_role'],response['galaxy_role'])
        self.assertEqual(data['name'], response['name'])

        # Get item details
        url_detail = '/api/v0/services/{pk}/applications/{ps}'.format(pk=str(service.pk),ps=response['name'])
        response = self.get(url_detail)
        self.assertEqual(data['name'],response['name'])
        self.assertEqual(data['galaxy_role'],response['galaxy_role'])

        # Change item details
        data = {
            'galaxy_role': 'extra',
            'name': 'second',
        }
        response = self.put(url_detail,data=data)
        self.assertEqual(response['name'],data['name'])
        self.assertEqual(response['galaxy_role'],data['galaxy_role'])

        # Change item details
        url_detail = '/api/v0/services/{pk}/applications/{ps}'.format(pk=str(service.pk),ps=response['name'])
        data={
            'galaxy_role': 'turbo',
        }
        response = self.patch(url_detail, data=data)
        data = {
            'galaxy_role': 'turbo',
            'name': 'second',
        }
        self.assertEqual(response['name'],data['name'])
        self.assertEqual(response['galaxy_role'],data['galaxy_role'])

        data={
            'name': 'third'
        }
        response = self.patch(url_detail,data=data)
        data = {
            'galaxy_role': 'turbo',
            'name': 'third',
        }
        self.assertEqual(response['name'],data['name'])
        self.assertEqual(response['galaxy_role'],data['galaxy_role'])


        # Delete item
        data = {
            'galaxy_role': 'turbo',
            'name': 'third'
        }
        url_detail = '/api/v0/services/{pk}/applications/{ps}'.format(pk=str(service.pk),ps=response['name'])
        response = self.delete(url=url_detail)
        self.assertEqual(data['galaxy_role'],response['galaxy_role'])
        self.assertEqual(data['name'],response['name'])


        service.delete()

    def test_user(self):
        from onelove.models import User

        # Prepare
        url_list = 'api/v0/users'

    def test_task(self):
        from onelove.models import Task
        url_list = '/api/v0/tasks'

        # Get empty list
        response = self.get(url=url_list)
        self.assertEqual(response, [])
