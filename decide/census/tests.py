import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from tablib import Dataset
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os

from .models import Census
from base import mods
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        rows = [
            [None, 1, 2, 'PABLO', 'PÉREZ GARCÍA', 'BILBAO', 'PAÍS VASCO', 'HOMBRE', '1992', 'SOLTERO', 'HETEROSEXUAL', 1],
            [None, 2, 3, 'CARLA', 'LÓPEZ VEGA', 'ALICANTE', 'COMUNIDAD VALENCIABA', 'MUJER', '1980', 'CASADA', 'HETEROSEXUAL', 0],
            [None, 3, 4, 'TINA', 'MORENO DÍAZ', 'LUGO', 'GALICIA', 'MUJER', '1998', 'SOLTERA', 'BISEXUAL', 1],
        ]

        for row in rows:
            value = Census(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                    row[9],
                    row[10],
                    row[11]
                    )
            value.save()
            
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_store_census(self):
        c=Census.objects.all()

        self.assertEqual(Census.objects.count(), 3)
        self.assertEqual(c[0].city, "BILBAO")
        self.assertEqual(c[1].gender, "MUJER")
        self.assertEqual(c[2].works, 1)

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

    # def test_import_census(self):
    #     #data = SimpleUploadedFile("static/census_data.xlsx", "file_content", content_type="mimetype")
    #     data_file_path = os.path.join(os.path.dirname(__file__), "census_data.xlsx")
    #     myfile = open(data_file_path)
    #     self.client.post(reverse('importer/'), {'myfile': myfile})
    #     # some important assertions ...

    #     self.assertEqual(Census.objects.count(), 10)
