import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from tablib import Dataset

from .models import Census
from base import mods
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    # def setUp(self):
    #     super().setUp()
    #     self.census = Census(voting_id=1, voter_id=1)
    #     self.census.save()

    # def tearDown(self):
    #     super().tearDown()
    #     self.census = None

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

    def test_importer_census(self):
        rows = [
            ['14', '1', '11', 'PABLO', 'PÉREZ GARCÍA', 'BILBAO', 'PAÍS VASCO', 'HOMBRE', '1992', 'SOLTERO', 'HETEROSEXUAL', '1'],
            ['15', '2', '12', 'CARLA', 'LÓPEZ VEGA', 'ALICANTE', 'COMUNIDAD VALENCIABA', 'MUJER', '1980', 'CASADA', 'HETEROSEXUAL', '0'],
            ['16', '3', '13', 'TINA', 'MORENO DÍAZ', 'LUGO', 'GALICIA', 'MUJER', '1998', 'SOLTERA', 'BISEXUAL', '1'],
            ['17', '4', '14', 'ALEX', 'MICHEL RODRÍGUEZ', 'PAMPLONA', 'NAVARRA', 'HOMBRE', '2002', 'SOLTERO', 'HETEROSEXUAL', '0'],
        ]

        dataset = tablib.Dataset(*rows, headers=self.headers)
        result = self.resource.import_data(
            dataset, dry_run=True, use_transactions=True,
            collect_failed_rows=True,
        )

        # Deberíamos obtener 1 línea bien y 1 línea fallada
        self.assertEqual(len(result.failed_dataset), 1)
        self.assertEqual(len(result.valid_rows()), 3)