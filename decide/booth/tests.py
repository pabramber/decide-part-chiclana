from base.tests import BaseTestCase
from django.contrib.auth.models import User


class BoothTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_listvoting(self):
        #Create user, voting and census
        u = User(username='1234')
        u.set_password('egc.decide')
        u.save()
        data = {'username': '1234', 'password': 'egc.decide'}
        self.client.post('/authentication/login/', data, format='json')
        response =self.client.get('/booth/')
        self.assertEqual(response.status_code, 200)
