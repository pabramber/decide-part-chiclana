
import random
import itertools
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from django.core.exceptions import ValidationError

import urllib.request


class VotingTestCase(BaseTestCase):
    
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    
    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)
     
    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting')
        v.save()
        v.question.add(q)

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        questions = list(v.question.all())

        for question in questions:
            for opt in QuestionOption.objects.filter(question=question):
                clear[opt.number] = 0
                for i in range(random.randint(0, 5)):
                    a, b = self.encrypt_msg(opt.number, v)
                    data = {
                        'voting': v.id,
                        'voter': voter.voter_id,
                        'vote': { 'a': a, 'b': b },
                    }
                    clear[opt.number] += 1
                    user = self.get_or_create_user(voter.voter_id)
                    self.login(user=user.username)
                    voter = voters.pop()
                    mods.post('store', json=data)
        return clear
    
    # Test de votación por preferencia con 2 opciones
    def test_create_ranked_question_with_two_options(self):
        question = Question(
            desc='test question 1', 
            type='R',
        )
        question.save()

        option1 = QuestionOption(question = question, option='op1')
        option1.save()
        option2 = QuestionOption(question = question, option='op2')
        option2.save()
        question.create_ordination = True
        question.save()

        test1 = Question.objects.get(desc='test question 1').options.all()
        self.assertEqual(test1.count(), 2)
        self.assertEqual(test1[0].option, 'op1, op2, ')
        self.assertEqual(test1[1].option, 'op2, op1, ')


    # Test de votación por preferencia con 3 opciones
    def test_create_ranked_question_with_three_options(self):
        question = Question(
            desc='test question 2', 
            type='R',
        )
        question.save()

        option1 = QuestionOption(question = question, option='op1')
        option1.save()
        option2 = QuestionOption(question = question, option='op2')
        option2.save()
        option3 = QuestionOption(question = question, option='op3')
        option3.save()
        question.create_ordination = True
        question.save()

        test2 = Question.objects.get(desc='test question 2').options.all()
        possible_ordenations = ['op1, op2, op3, ', 'op1, op3, op2, ', 'op2, op1, op3, ',
             'op2, op3, op1, ', 'op3, op1, op2, ', 'op3, op2, op1, ']

        self.assertEqual(test2.count(), 6)
        for opcion in test2:
            possible_ordenations.remove(opcion.option)
            
        self.assertEqual(len(possible_ordenations), 0)

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.all():
            for qo in QuestionOption.objects.filter(question=q):
                self.assertEqual(tally.get(qo.number, 0), clear.get(qo.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'postproc_type': 'IDENTITY',
            'number_seats': 1
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied') 
    def test_put_future_date(self):
        #creacion de votacion:
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        v.future_start = datetime.strptime('2023-08-09 01:01:01', "%Y-%m-%d %H:%M:%S")
        v.save()
        return v

    def test_put_future_date(self):
        #creacion de votacion:
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting')
        
        v.save()
        v.question.add(q)
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        v.future_stop = datetime.strptime('2023-08-09 01:01:01', "%Y-%m-%d %H:%M:%S")
        v.save()
        return v
    
    # Testing yes/no question feature
    def test_create_yes_no_question(self):
        q = Question(desc='Yes/No question test', type='B')
        q.save()

        self.assertEquals(len(q.options.all()), 2)
        self.assertEquals(q.type, 'B')
        self.assertEquals(q.options.all()[0].option, 'Sí')
        self.assertEquals(q.options.all()[1].option, 'No')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)

    # Adding options other than yes and no manually
    def test_create_yes_no_question_with_other_options(self):
        q = Question(desc='Yes/No question test', type='B')
        q.save()
        qo1 = QuestionOption(question = q, option = 'First option')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Second option')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Third option')
        qo3.save()

        self.assertEquals(len(q.options.all()), 2)
        self.assertEquals(q.type, 'B')
        self.assertEquals(q.options.all()[0].option, 'Sí')
        self.assertEquals(q.options.all()[1].option, 'No')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)

    # Testing score question feature
    def test_create_score_question(self):
        q = Question(desc='Score question test', type='S')
        q.save()
        self.assertEquals(len(q.options.all()), 11)
        self.assertEquals(q.type, 'S')
        for i in range(0, 11):
                self.assertEquals(q.options.all()[i].option, str(i))
                self.assertEquals(q.options.all()[i].number, i+2)
    
    # Testing save voting file
    def test_save_voting_file_200(self):
        self.login()
        voting = self.create_voting()
        
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')       

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        data = {'action': 'save'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Saved voting file')

    def test_save_voting_file_not_started_400(self):
        self.login()
        voting = self.create_voting()

        data = {'action': 'save'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not started')

    def test_save_voting_file_not_stopped_400(self):
        self.login()
        voting = self.create_voting()

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')       

        data = {'action': 'save'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

    def test_save_voting_file_not_tallied_400(self):
        self.login()
        voting = self.create_voting()

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')       

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        data = {'action': 'save'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting has not being tallied')

    
    def test_create_image_question_success(self):
        url_one = "https://wallpapercave.com/uwp/uwp1871846.png"
        url_two = "https://wallpapercave.com/uwp/uwp2004429.jpeg"
        question = Question(desc='Image question test', type='I')
        question.save()
        qo_one = QuestionOption(question=question, option=url_one)
        qo_two = QuestionOption(question=question, option=url_two)
        qo_one.save()
        qo_two.save()
        self.assertEquals(len(question.options.all()), 2)
        self.assertEquals(question.options.all()[0].option, url_one)
        self.assertEquals(question.options.all()[1].option, url_two)
    
    def test_create_image_question_failure_no_url(self):
        not_url = "This is not a url!!!"
        question = Question(desc='Image question test', type='I')
        question.save()
        qo_one = QuestionOption(question=question, option=not_url)
        try:
            qo_one.clean()
            qo_one.save()
        except ValidationError as e:
            self.assertEquals(e.message, 'Enter a valid URL.')
        self.assertEquals(len(question.options.all()), 0)
    def test_create_image_question_failure_destination_unreachable(self):
        not_url = "http://www.google.com"
        question = Question(desc='Image question test', type='I')
        question.save()
        qo_one = QuestionOption(question=question, option=not_url)
        try:
            qo_one.clean()
            qo_one.save()
        except ValidationError as e:
            self.assertEquals(e.message, 'Url does not contain a compatible image')
        self.assertEquals(len(question.options.all()), 0)

