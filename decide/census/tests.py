import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from tablib import Dataset
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os

from timeit import default_timer
from .models import Census
from base import mods
from base.tests import BaseTestCase
from .forms import CreationCensusForm
from django.test import SimpleTestCase

class CensusFrontendTestCase(BaseTestCase):
    def test_creation_census(self):
        censo = Census.objects.create(voting_id=1, voter_id=2, name='PABLO', surname='PÉREZ GARCÍA',city= 'BILBAO', a_community='PAÍS VASCO', gender='HOMBRE', born_year=1992, civil_state='SOLTERO', sexuality='HETEROSEXUAL',works= 1)
        censo.save()
        self.assertEqual(censo.name, "PABLO")
        self.assertEqual(censo.voting_id, 1)
        self.assertEqual(censo.voter_id, 2)
        self.assertEqual(censo.surname, 'PÉREZ GARCÍA')
        self.assertEqual(censo.city, 'BILBAO')
        self.assertEqual(censo.a_community, 'PAÍS VASCO')
        self.assertEqual(censo.gender, 'HOMBRE')
        self.assertEqual(censo.born_year, 1992)
        self.assertEqual(censo.civil_state, 'SOLTERO')
        self.assertEqual(censo.sexuality, 'HETEROSEXUAL')
        self.assertEqual(censo.works, 1)


class CensusFrontendFormCreationTestCase(SimpleTestCase):

    def test_creation_form_no_data(self):
        form = CreationCensusForm(data={})
        self.assertFalse(form.is_valid())


#class CensusTestCase(BaseTestCase):

    # def setUp(self):
    #     super().setUp()
    #     self.census = Census(voting_id=1, voter_id=1)
    #     self.census.save()

    # def tearDown(self):
    #     super().tearDown()
    #     self.census = None
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

    def test_import_wrong_format(self):
        myfile = open('census/static/census_formato_incorrecto.ods', 'rb')
        data = {
            'myfile': myfile
        }
        response = self.client.post(reverse('importer'), data)

        # (3 son la cantidad de registros que había antes)
        # Es decir, no se ha añadido ningún registro más, el import no se ha realizado
        self.assertEqual(Census.objects.count(), 3)

    def test_import_success(self):
        myfile = open('census/static/census_data.xlsx', 'rb')
        data = {
            'myfile': myfile
        }
        response = self.client.post(reverse('importer'), data)

        c=Census.objects.all()
        # El Excel contiene 10 registros, más los 3 anteriores = 13
        self.assertEqual(Census.objects.count(), 13)
        self.assertEqual(c[3].name, "SERGIO")
        self.assertEqual(c[9].a_community, "EXTREMADURA")

    def test_export_success(self):
        myfile = open('census/static/ReporteAutorExcel.xlsx', 'rb')
        data = {
            'myfile': myfile
        }
        response = self.client.post(reverse('reporte'), data)

        
        # El Excel contiene está vacío, con los 3 anteriores = 3
        self.assertEqual(Census.objects.count(), 3)
        

        



    # def test_import_census(self):
    #     #data = SimpleUploadedFile("static/census_data.xlsx", "file_content", content_type="mimetype")
    #     data_file_path = os.path.join(os.path.dirname(__file__), "census_data.xlsx")
    #     myfile = open(data_file_path)
    #     self.client.post(reverse('importer/'), {'myfile': myfile})
    #     # some important assertions ...

    #     self.assertEqual(Census.objects.count(), 10)

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


    # def test_filter_census(self):
    #     inicio = default_timer()
    #     id=1
    #     censo = Census.objects.get(voting_id=int(id))
    #     self.assertEqual(censo.voting_id, 1)
    #     self.assertEqual(censo.voter_id, 1)
    #     fin = default_timer()
    #     print("test_filter_nameOK: " + str(fin-inicio) + "s")

    # def test_filter_censusName(self):
    #     inicio = default_timer()
    #     id=1
    #     censo = Census.objects.get(voting_id=int(id))
    #     self.assertEqual(censo.name, "Roger")
    #     self.assertEqual(censo.surname, "Marin")
    #     fin = default_timer()
    #     print("test_filter_nameOK: " + str(fin-inicio) + "s")

