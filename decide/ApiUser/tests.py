from django.test import TestCase
from base.tests import BaseTestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your tests here.
class ApiUserTestCase(TestCase):
    multi_db = True
    def setUp(self):
        super().setUp()
        username1= "username1"
        password1="password1"
        email1="myemail1@gmail.com"
        first_name1="first_name1"
        last_name1="last_name1"
        is_staff1=False
        self.user = User(username=username1,password=password1,email=email1,first_name=first_name1,
        last_name=last_name1,is_staff=is_staff1)
        self.user.save()

        username2= "username2"
        password2="password2"
        email2="myemail2@gmail.com"
        first_name2="first_name2"
        last_name2="last_name2"
        is_staff2=True
        self.user2 = User(username=username2,password=password2,email=email2,first_name=first_name2,
        last_name=last_name2,is_staff=is_staff2)
        self.user2.save()

    def tearDown(self):
        super().tearDown()
        self.user=None

    def test_list_users(self):
        url = '/api/user/list'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["Message"], "New user added")

        self.assertEqual(response.data["user"][0].get('id'),1)
        self.assertEqual(response.data["user"][0].get('username'),'username1')
        self.assertEqual(response.data["user"][0].get('first_name'),'first_name1')
        self.assertEqual(response.data["user"][0].get('last_name'),'last_name1')
        self.assertEqual(response.data["user"][0].get('email'),'myemail1@gmail.com')
        self.assertEqual(response.data["user"][0].get('password'),'password1')

        self.assertEqual(response.data["user"][1].get('id'),2)
        self.assertEqual(response.data["user"][1].get('username'),'username2')
        self.assertEqual(response.data["user"][1].get('first_name'),'first_name2')
        self.assertEqual(response.data["user"][1].get('last_name'),'last_name2')
        self.assertEqual(response.data["user"][1].get('email'),'myemail2@gmail.com')
        self.assertEqual(response.data["user"][1].get('password'),'password2')
    
    def test_user_details_positive(self):
        user=self.user
        url = '/api/user/'+str(user.id)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["Message"], "This are the details of the searched user:")
        self.assertEqual(response.data["user"].get('id'),user.id)
        self.assertEqual(response.data["user"].get('username'),user.username)
        self.assertEqual(response.data["user"].get('first_name'),user.first_name)
        self.assertEqual(response.data["user"].get('last_name'),user.last_name)
        self.assertEqual(response.data["user"].get('email'),user.email)
        self.assertEqual(response.data["user"].get('password'),user.password)

    def test_user_details_negative(self):
        url = '/api/user/'+'150'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data["Message"], "The user  can not be found in Decide application.")
    
    def test_user_staff(self):
        user=self.user2
        username = self.user2.username.upper()
        url = '/api/user/staff/'+str(user.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["Message"], "The user "+username+" is a staff member")
        user=self.user
        username = self.user.username.upper()
        url = '/api/user/staff/'+str(user.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["Message"], "The user "+username+" is not a staff member")

    def test_user_is_staff_negative(self):
        
        url = '/api/user/staff/'+str(150)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data["Message"], "The user  can not be found in Decide application.")
    
    def test_positive_post_add_new_user(self):
        url = '/api/user/list'
        username1= "username3"
        password1="password4"
        email1="myemail3@gmail.com"
        first_name1="first_name3"
        last_name1="last_name4"
        is_staff1=True
        
        data = {'username':username1,'first_name':first_name1,'last_name':last_name1,
        'password':password1,'email':email1,'is_staff': is_staff1}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, 200)
        
        json_response=response.json()
        message=json_response.get('Message')
        user_json=json_response.get('user')
        self.assertEqual(message, 'New user added')
        
        self.assertEqual(user_json[0]['username'], username1)
        self.assertEqual(user_json[0]['first_name'], first_name1)
        self.assertEqual(user_json[0]['last_name'], last_name1)
        self.assertEqual(user_json[0]['email'], email1)
        self.assertEqual(user_json[0]['is_staff'], is_staff1)
        self.assertEqual(user_json[0]['is_active'], True)
        self.assertNotEqual(user_json[0]['password'], password1)

    def test_negative_post_add_new_user(self):
        url = '/api/user/list'
        username1= "username1"
        password1="password4"
        email1="myemail3@gmail.com"
        first_name1="first_name3"
        last_name1="last_name4"
        is_staff1=True
        
        data = {'username':username1,'first_name':first_name1,'last_name':last_name1,
        'password':password1,'email':email1,'is_staff': is_staff1}
        try:
            response = self.client.post(url,data,format='json')
        except IntegrityError as e: 
            self.assertRaises(IntegrityError)