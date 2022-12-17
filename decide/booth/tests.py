from base.tests import BaseTestCase
from django.contrib.auth.models import User
from base import mods


class BoothTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        mods.mock_query(self.client)
        u = User(username='1234')
        u.set_password('egc.decide')
        u.save()

    def tearDown(self):
        super().tearDown()

    def test_list_voting(self):
        data = {'username': '1234', 'password': 'egc.decide'}
        self.client.post('/authentication/login/', data, format='json')
        response =self.client.get('/booth/')
        self.assertEqual(response.status_code, 302)