from django.test import TestCase
from base.tests import BaseTestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import models
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

    def test_update_user(self):
        userList = User.objects.all().values()
        user=userList[0]
        url = '/api/user/'+str(user.get('id'))
        new_username= "new_username"
        new_password="new_password"
        new_email="newemail@gmail.com"
        new_firstname="new_firstname"
        new_lastname="new_lastname"
        new_is_staff=True
        data = {'username':new_username,'first_name':new_firstname,'last_name':new_lastname,
        'password':new_password,'email':new_email,'is_staff': new_is_staff}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 415)
    
    def test_positive_delete_user(self):
        code=204
        userList = User.objects.all().values()
        user=userList[0]
        url = '/api/user/'+str(user.get('id'))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, code)
        userDeleted = User.objects.all().filter(id=user.get('id')).values()
        self.assertEqual(len(userDeleted),0)

    def test_negative_delete_user(self):
        code=404
        userList = User.objects.all().values()
        user=userList[0]
        url = '/api/user/'+str(100)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, code)

            
    def test_positive_user_exist(self):
        user=self.user2
        url = '/api/user/exists/'+user.username
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["Message"], "The user with username = "+user.username+" exist in our database.")
        userObtained=response.data["user"]
        self.assertEqual(user.username, userObtained["username"])
        self.assertEqual(user.first_name, userObtained["first_name"])

    def test_negative_user_exist(self):
        user=self.user2
        username=user.username+"notexist"
        url = '/api/user/exists/'+username
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 204)
        message="The user with username = "+username+" does NOT exist in our database."
        self.assertEqual(response.data["Message"], message)