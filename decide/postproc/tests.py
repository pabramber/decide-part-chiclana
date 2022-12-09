from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhondt(self):
        data = {
            'type': 'DHONDT',
            'seats': 7,
            'options': [
                { 'option': 'Policital party 2', 'number': 1, 'votes': 280000 },
                { 'option': 'Policital party 4', 'number': 2, 'votes': 60000 },
                { 'option': 'Policital party 1', 'number': 3, 'votes': 340000 },
                { 'option': 'Policital party 5', 'number': 4, 'votes': 15000 },
                { 'option': 'Policital party 3', 'number': 5, 'votes': 160000 },
            ]
        }

        expected_result = [
            { 'option': 'Policital party 1', 'number': 3, 'votes': 340000, 'postproc': 3 },
            { 'option': 'Policital party 2', 'number': 1, 'votes': 280000, 'postproc': 3 },
            { 'option': 'Policital party 3', 'number': 5, 'votes': 160000, 'postproc': 1 },
            { 'option': 'Policital party 4', 'number': 2, 'votes': 60000, 'postproc': 0 },
            { 'option': 'Policital party 5', 'number': 4, 'votes': 15000, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_droop(self):
        data = {
            'type': 'DROOP',
            'seats': 21,
            'options': [
                { 'option': 'Policital party 2', 'number': 1, 'votes': 311000 },
                { 'option': 'Policital party 4', 'number': 2, 'votes': 73000 },
                { 'option': 'Policital party 1', 'number': 3, 'votes': 391000 },
                { 'option': 'Policital party 5', 'number': 4, 'votes': 27000 },
                { 'option': 'Policital party 3', 'number': 5, 'votes': 184000 },
                { 'option': 'Policital party 7', 'number': 6, 'votes': 2000 },
                { 'option': 'Policital party 6', 'number': 7, 'votes': 12000 },
            ]
        }

        expected_result = [
            { 'option': 'Policital party 1', 'number': 3, 'votes': 391000, 'postproc': 8 },
            { 'option': 'Policital party 2', 'number': 1, 'votes': 311000, 'postproc': 7 },
            { 'option': 'Policital party 3', 'number': 5, 'votes': 184000, 'postproc': 4 },
            { 'option': 'Policital party 4', 'number': 2, 'votes': 73000, 'postproc': 2 },
            { 'option': 'Policital party 5', 'number': 4, 'votes': 27000, 'postproc': 0 },
            { 'option': 'Policital party 6', 'number': 7, 'votes': 12000, 'postproc': 0 },
            { 'option': 'Policital party 7', 'number': 6, 'votes': 2000, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_hare(self):
        data = {
            'type': 'HARE',
            'seats': 21,
            'options': [
                { 'option': 'Policital party 2', 'number': 1, 'votes': 311000 },
                { 'option': 'Policital party 4', 'number': 2, 'votes': 73000 },
                { 'option': 'Policital party 1', 'number': 3, 'votes': 391000 },
                { 'option': 'Policital party 5', 'number': 4, 'votes': 27000 },
                { 'option': 'Policital party 3', 'number': 5, 'votes': 184000 },
                { 'option': 'Policital party 7', 'number': 6, 'votes': 2000 },
                { 'option': 'Policital party 6', 'number': 7, 'votes': 12000 },
            ]
        }

        expected_result = [
            { 'option': 'Policital party 1', 'number': 3, 'votes': 391000, 'postproc': 8 },
            { 'option': 'Policital party 2', 'number': 1, 'votes': 311000, 'postproc': 6 },
            { 'option': 'Policital party 3', 'number': 5, 'votes': 184000, 'postproc': 4 },
            { 'option': 'Policital party 4', 'number': 2, 'votes': 73000, 'postproc': 2 },
            { 'option': 'Policital party 5', 'number': 4, 'votes': 27000, 'postproc': 1 },
            { 'option': 'Policital party 6', 'number': 7, 'votes': 12000, 'postproc': 0 },
            { 'option': 'Policital party 7', 'number': 6, 'votes': 2000, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_hare_01(self):

        data = {
            'type': 'HARE',
            'seats': 21,
            'options': [
                { 'option': 'Policital party 1', 'number': 1, 'votes': 264793 },
                { 'option': 'Policital party 2', 'number': 2, 'votes': 654046 },
            ]
            
        }

        expected_result = [

            { 'option': 'Policital party 2', 'number': 2, 'votes': 654046, 'postproc': 15 },
            { 'option': 'Policital party 1', 'number': 1, 'votes': 264793, 'postproc': 6 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_hare_02(self):
        data = {
            'type': 'HARE',
            'seats': 21,
            'options': [
                { 'option': 'Policital party 1', 'number': 1, 'votes': 2510 },
                { 'option': 'Policital party 2', 'number': 2, 'votes': 300 },
                { 'option': 'Policital party 3', 'number': 3, 'votes': 245034 },
                { 'option': 'Policital party 4', 'number': 4, 'votes': 200001 },
                { 'option': 'Policital party 5', 'number': 5, 'votes': 14 },
                { 'option': 'Policital party 6', 'number': 6, 'votes': 20145 },
            ]
            
        }

        expected_result = [
            { 'option': 'Policital party 3', 'number': 3, 'votes': 245034, 'postproc': 11 },
            { 'option': 'Policital party 4', 'number': 4, 'votes': 200001, 'postproc': 9 },
            { 'option': 'Policital party 6', 'number': 6, 'votes': 20145, 'postproc': 1 },
            { 'option': 'Policital party 1', 'number': 1, 'votes': 2510, 'postproc': 0 },
            { 'option': 'Policital party 2', 'number': 2, 'votes': 300, 'postproc': 0 }, 
            { 'option': 'Policital party 5', 'number': 5, 'votes': 14, 'postproc': 0 },
            
        ]
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_hare_03(self):
        data = {
            'type': 'HARE',
            'seats': 21,
            'options': [
                { 'option': 'Policital party 1', 'number': 1, 'votes': 2510 },
                { 'option': 'Policital party 2', 'number': 2, 'votes': 6540 },
                { 'option': 'Policital party 3', 'number': 3, 'votes': 0 },
                { 'option': 'Policital party 4', 'number': 4, 'votes': 12046 },
                { 'option': 'Policital party 5', 'number': 5, 'votes': 14 },
                { 'option': 'Policital party 6', 'number': 6, 'votes': 20145 },
            ]

        }

        expected_result = [
            { 'option': 'Policital party 6', 'number': 6, 'votes': 20145, 'postproc': 10 },
            { 'option': 'Policital party 4', 'number': 4, 'votes': 12046, 'postproc': 6 },
            { 'option': 'Policital party 2', 'number': 2, 'votes': 6540, 'postproc': 4 },
            { 'option': 'Policital party 1', 'number': 1, 'votes': 2510, 'postproc': 1 },
            { 'option': 'Policital party 5', 'number': 5, 'votes': 14, 'postproc': 0 },
            { 'option': 'Policital party 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_hare_04(self):
        data = {
            'type': 'HARE',
            'seats': 22,
            'options': [
                { 'option': 'Policital party 1', 'number': 1, 'votes': 2659 },
                { 'option': 'Policital party 2', 'number': 2, 'votes': 0 },
                { 'option': 'Policital party 3', 'number': 3, 'votes': 0 },
                { 'option': 'Policital party 4', 'number': 4, 'votes': 0 },
                { 'option': 'Policital party 5', 'number': 5, 'votes': 0 },
                { 'option': 'Policital party 6', 'number': 6, 'votes': 2659 },
            ]
        }

        expected_result = [
            { 'option': 'Policital party 1', 'number': 1, 'votes': 2659, 'postproc': 11 },
            { 'option': 'Policital party 6', 'number': 6, 'votes': 2659, 'postproc': 11 },
            { 'option': 'Policital party 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 4', 'number': 4, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 5', 'number': 5, 'votes': 0, 'postproc': 0 },
            
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    

    def test_hare_05(self):
        data = {
            'type': 'HARE',
            'seats': 21,
            'options': [
                { 'option': 'Policital party 1', 'number': 1, 'votes': 2659 },
                { 'option': 'Policital party 2', 'number': 2, 'votes': 0 },
                { 'option': 'Policital party 3', 'number': 3, 'votes': 0 },
                { 'option': 'Policital party 4', 'number': 4, 'votes': 0 },
                { 'option': 'Policital party 5', 'number': 5, 'votes': 0 },
                { 'option': 'Policital party 6', 'number': 6, 'votes': 0 },
            ]
            
        }

        expected_result = [
            { 'option': 'Policital party 1', 'number': 1, 'votes': 2659, 'postproc': 21 },
            { 'option': 'Policital party 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 4', 'number': 4, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 5', 'number': 5, 'votes': 0, 'postproc': 0 },
            { 'option': 'Policital party 6', 'number': 6, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    

    def test_borda(self):
        
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular','number':1, 'positions': [1,1,3,2],'votes': 0},
                {'option': 'Psoe','number':2, 'positions': [2,3,4,3],'votes': 0},
                {'option': 'Podemos','number':3, 'positions': [3,4,1,4],'votes': 0},
                {'option': 'Ciudadanos','number':4, 'positions': [4,2,2,1],'votes': 0},
            ]
        }

        expected_result = [
            {'option': 'Popular','number':1,'positions': [1,1,3,2], 'votes': 13},
            {'option': 'Psoe','number':2,'positions': [2,3,4,3], 'votes': 8},
            {'option': 'Podemos','number':3,'positions': [3,4,1,4], 'votes': 8},
            {'option': 'Ciudadanos','number':4,'positions': [4,2,2,1], 'votes': 11},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    def test_reinforced_imperial(self):
        data = {
            'type': 'REINFORCED_IMPERIAL',
            'seats': 17,
            'options': [
                { 'option': 'Policital party 2', 'number': 1, 'votes': 311000 },
                { 'option': 'Policital party 4', 'number': 2, 'votes': 73000 },
                { 'option': 'Policital party 1', 'number': 3, 'votes': 391000 },
                { 'option': 'Policital party 5', 'number': 4, 'votes': 27000 },
                { 'option': 'Policital party 3', 'number': 5, 'votes': 184000 },
                { 'option': 'Policital party 7', 'number': 6, 'votes': 2000 },
                { 'option': 'Policital party 6', 'number': 7, 'votes': 12000 },
            ]
        }

        expected_result = [
            { 'option': 'Policital party 1', 'number': 3, 'votes': 391000, 'postproc': 7 },
            { 'option': 'Policital party 2', 'number': 1, 'votes': 311000, 'postproc': 6 },
            { 'option': 'Policital party 3', 'number': 5, 'votes': 184000, 'postproc': 3 },
            { 'option': 'Policital party 4', 'number': 2, 'votes': 73000, 'postproc': 1 },
            { 'option': 'Policital party 5', 'number': 4, 'votes': 27000, 'postproc': 0 },
            { 'option': 'Policital party 6', 'number': 7, 'votes': 12000, 'postproc': 0 },
            { 'option': 'Policital party 7', 'number': 6, 'votes': 2000, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)