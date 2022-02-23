from rest_framework.test import APIClient

from organization.models import Organization
from organization.tests import base_test


# Post Method Test
class OrganizationTestCreateCase(base_test.NewUserTestCase):
    """
    Organization Create API Test Case
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_organization_create_api(self):
        self.create_organization = self.client.post('/api/organization/',
                                                    {'name': 'Ogul Tutuncu',
                                                     'established_on': '1998-08-03',
                                                     'registration_code': '123456',
                                                     'address': 'Warsaw,Poland'
                                                     },
                                                    format='json')

        self.assertEquals(self.create_organization.status_code, 201)
        self.assertTrue('Ogul Tutuncu' in self.create_organization.json()['data']['name'])
        self.assertTrue('1998-08-03' in self.create_organization.json()['data']['established_on'])
        self.assertTrue('123456' in self.create_organization.json()['data']['registration_code'])
        self.assertTrue('Warsaw,Poland' in self.create_organization.json()['data']['address'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


# Get Method Test
class OrganizationTestListCase(base_test.NewUserTestCase):
    """
    Organization List API Test Case
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create a new Organization
        self.organization = Organization.objects.create(name='Dinesh Kumar',
                                                        established_on='1998-10-22',
                                                        registration_code='111111')

    def test_organization_list_api(self):
        self.list_organizations = self.client.get('/api/organization/', format='json')
        self.assertEquals(self.list_organizations.status_code, 200)
        self.assertTrue('Dinesh Kumar' in self.list_organizations.json()['results'][0]['name'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


# Get Method Test
class OrganizationTestReadByIdCase(base_test.NewUserTestCase):
    """
    Organization Read API by Id Test Case
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.organization = Organization.objects.create(name='Dinesh Kumar',
                                                        established_on='1998-10-22',
                                                        registration_code='111222')

    def test_organization_read_by_id_api(self):
        self.read_organization_by_id = self.client.get(f'/api/organization/{self.organization.id}', format='json')

        self.assertEquals(self.read_organization_by_id.status_code, 200)
        self.assertTrue('Dinesh Kumar' in self.read_organization_by_id.json()['name'])
        self.assertTrue('1998-10-22' in self.read_organization_by_id.json()['established_on'])
        self.assertTrue('111222' in self.read_organization_by_id.json()['registration_code'])

    def tearDown(self):
        self.client.logout()
        self.organization.delete()
        super().tearDown()


# Put Method Test
class OrganizationTestUpdateByIdCase(base_test.NewUserTestCase):
    """
    Organization Update API By Id Test Case
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.organization = Organization.objects.create(name='Dinesh Kumar',
                                                        established_on='1998-10-22',
                                                        registration_code='222334')

    def test_organization_update_by_id_api(self):
        self.update_organization_by_id = self.client.put(f'/api/organization/{self.organization.id}',
                                                         {'name': 'Dinesh "the COO" Kumar',
                                                          'established_on': '1998-10-21',
                                                          'registration_code': '475321'},
                                                         format='json')

        self.assertEquals(self.update_organization_by_id.status_code, 200)
        self.assertTrue(self.update_organization_by_id.json()['status'], True)
        self.assertEquals(self.update_organization_by_id.json()['message'], 'Organization Updated!')
        self.assertEquals(self.update_organization_by_id.json()['data']['name'], 'Dinesh "the COO" Kumar')
        self.assertEquals(self.update_organization_by_id.json()['data']['registration_code'], '475321')
        self.assertEquals(self.update_organization_by_id.json()['data']['established_on'], '1998-10-21')

    def tearDown(self):
        self.client.logout()
        self.organization.delete()
        super().tearDown()


# Delete Method Test
class OrganizationTestDeleteByIdCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create Organization
        self.organization = Organization.objects.create(name='Dinesh Kumar',
                                                        established_on='1998-10-21',
                                                        registration_code='159638')

    def test_organization_delete_by_id_api(self):
        self.delete_organization_by_id = self.client.delete(f'/api/organization/{self.organization.id}',
                                                            format='json')

        self.assertEquals(self.delete_organization_by_id.status_code, 204)

    def tearDown(self):
        self.client.logout()
        super().tearDown()
