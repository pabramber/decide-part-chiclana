import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from timeit import default_timer
from .models import Census
from base import mods
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    # def test_check_vote_permissions(self):
    #     response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(), 'Invalid voter')

    #     response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), 'Valid voter')

    # def test_list_voting(self):
    #     response = self.client.get('/census/?voting_id={}'.format(1), format='json')
    #     self.assertEqual(response.status_code, 401)

    #     self.login(user='noadmin')
    #     response = self.client.get('/census/?voting_id={}'.format(1), format='json')
    #     self.assertEqual(response.status_code, 403)

    #     self.login()
    #     response = self.client.get('/census/?voting_id={}'.format(1), format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), {'voters': [1]})

    # def test_add_new_voters_conflict(self):
    #     data = {'voting_id': 1, 'voters': [1]}
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 401)

    #     self.login(user='noadmin')
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 403)

    #     self.login()
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 409)

    # def test_add_new_voters(self):
    #     data = {'voting_id': 2, 'voters': [1,2,3,4]}
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 401)

    #     self.login(user='noadmin')
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 403)

    #     self.login()
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    # def test_destroy_voter(self):
    #     data = {'voters': [1]}
    #     response = self.client.delete('/census/{}/'.format(1), data, format='json')
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(0, Census.objects.count())

    def test_filter_census(self):
        inicio = default_timer()
        id=1
        censo = Census.objects.get(voting_id=int(id))
        self.assertEqual(censo.voting_id, 1)
        self.assertEqual(censo.voter_id, 1)
        fin = default_timer()
        print("test_filter_nameOK: " + str(fin-inicio) + "s")

###
    # def test_filter_censusName(self):
    #     inicio = default_timer()
    #     id=1
    #     censo = Census.objects.get(voting_id=int(id))
    #     self.assertEqual(censo.name, "Roger")
    #     self.assertEqual(censo.surname, "Marin")
    #     fin = default_timer()
    #     print("test_filter_nameOK: " + str(fin-inicio) + "s")