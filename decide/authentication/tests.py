from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base.tests import BaseTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from .views import CustomUserCreationForm


from base import mods


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()
        print(token)
        token.update({'username': 'user1'})
        print(token)
        response = self.client.post('/authentication/register-api/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register-api/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register-api/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register-api/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )
    
class TestTestregisterPositive(TestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.cleaner = webdriver.Chrome(options=options)


        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()

        self.cleaner.quit()

        self.base.tearDown()
  
    def test_testregisterpositive(self):
        self.cleaner.get("http://127.0.0.1:8000/authentication/register/")
        self.cleaner.set_window_size(917, 1023)
        self.cleaner.find_element(By.ID, "id_username").click()

        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = "user"+str(delta.total_seconds()) 

        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("contrasenia12345")
        self.cleaner.find_element(By.ID, "id_password2").click()
        self.cleaner.find_element(By.ID, "id_password2").send_keys("contrasenia12345")
        self.cleaner.find_element(By.ID, "id_email").click()

        email = "test"+str(delta.total_seconds())+"@gm.com"

        self.cleaner.find_element(By.ID, "id_email").send_keys(email)
        self.cleaner.find_element(By.ID, "id_first_name").click()
        self.cleaner.find_element(By.ID, "id_first_name").send_keys("Jhon")
        self.cleaner.find_element(By.ID, "id_last_name").click()
        self.cleaner.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.cleaner.find_element(By.CSS_SELECTOR, ".btn").click()

        self.assertTrue(self.cleaner.current_url == "http://127.0.0.1:8000/")




class TestTestregisterNegativePassword(TestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.cleaner = webdriver.Chrome(options=options)


        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()

        self.cleaner.quit()

        self.base.tearDown()
  
    def test_testregister_negative_password_numeric(self):
        self.cleaner.get("http://127.0.0.1:8000/authentication/register/")
        self.cleaner.set_window_size(917, 1023)
        self.cleaner.find_element(By.ID, "id_username").click()

        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = "user"+str(delta.total_seconds()) 

        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("12345678")
        self.cleaner.find_element(By.ID, "id_password2").click()
        self.cleaner.find_element(By.ID, "id_password2").send_keys("12345678")
        self.cleaner.find_element(By.ID, "id_email").click()

        email = "test"+str(delta.total_seconds())+"@gm.com"

        self.cleaner.find_element(By.ID, "id_email").send_keys(email)
        self.cleaner.find_element(By.ID, "id_first_name").click()
        self.cleaner.find_element(By.ID, "id_first_name").send_keys("Jhon")
        self.cleaner.find_element(By.ID, "id_last_name").click()
        self.cleaner.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.cleaner.find_element(By.CSS_SELECTOR, ".btn").click()

        self.assertTrue(self.cleaner.current_url == "http://127.0.0.1:8000/authentication/register/")
        self.assertTrue( self.cleaner.find_element(By.CSS_SELECTOR, ".alert").text == "This password is entirely numeric")



class TestTestregisterNegativePasswordCommonly(TestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.cleaner = webdriver.Chrome(options=options)


        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()

        self.cleaner.quit()

        self.base.tearDown()


    def test_testregister_negative_password_commonly(self):
        self.cleaner.get("http://127.0.0.1:8000/authentication/register/")
        self.cleaner.set_window_size(917, 1023)
        self.cleaner.find_element(By.ID, "id_username").click()

        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = "user"+str(delta.total_seconds()) 

        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("qwertyui")
        self.cleaner.find_element(By.ID, "id_password2").click()
        self.cleaner.find_element(By.ID, "id_password2").send_keys("qwertyui")
        self.cleaner.find_element(By.ID, "id_email").click()

        email = "test"+str(delta.total_seconds())+"@gm.com"

        self.cleaner.find_element(By.ID, "id_email").send_keys(email)
        self.cleaner.find_element(By.ID, "id_first_name").click()
        self.cleaner.find_element(By.ID, "id_first_name").send_keys("Jhon")
        self.cleaner.find_element(By.ID, "id_last_name").click()
        self.cleaner.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.cleaner.find_element(By.CSS_SELECTOR, ".btn").click()

        self.assertTrue(self.cleaner.current_url == "http://127.0.0.1:8000/authentication/register/")
        self.assertTrue( self.cleaner.find_element(By.CSS_SELECTOR, ".alert").text == "This password is a commonly password")





class TestTestregisterNegativePasswordTooSimilar(TestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.cleaner = webdriver.Chrome(options=options)


        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()

        self.cleaner.quit()

        self.base.tearDown()


    def test_testregister_negative_password_too_similar(self):
        self.cleaner.get("http://127.0.0.1:8000/authentication/register/")
        self.cleaner.set_window_size(917, 1023)
        self.cleaner.find_element(By.ID, "id_username").click()

        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = "antonio"+str(delta.total_seconds()) 

        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("antonio"+str(delta.total_seconds()) )
        self.cleaner.find_element(By.ID, "id_password2").click()
        self.cleaner.find_element(By.ID, "id_password2").send_keys("antonio"+str(delta.total_seconds()) )
        self.cleaner.find_element(By.ID, "id_email").click()

        email = "test"+str(delta.total_seconds())+"@gm.com"

        self.cleaner.find_element(By.ID, "id_email").send_keys(email)
        self.cleaner.find_element(By.ID, "id_first_name").click()
        self.cleaner.find_element(By.ID, "id_first_name").send_keys("Jhon")
        self.cleaner.find_element(By.ID, "id_last_name").click()
        self.cleaner.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.cleaner.find_element(By.CSS_SELECTOR, ".btn").click()

        self.assertTrue(self.cleaner.current_url == "http://127.0.0.1:8000/authentication/register/")
        self.assertTrue( self.cleaner.find_element(By.CSS_SELECTOR, ".alert").text == "This password is too similar to your personal data")



class TestLoginPositive(TestCase):
  
  
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.cleaner = webdriver.Chrome(options=options)


        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()

        self.cleaner.quit()

        self.base.tearDown()
  
    def test_testlogin_positive(self):
        
        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = "userLogin"+str(delta.total_seconds())

        email = "testEmailLogin"+str(delta.total_seconds())+"@gm.com"

        self.cleaner.get("http://localhost:8000/authentication/register/")
        self.cleaner.set_window_size(917, 1023)
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("admin12345678")
        self.cleaner.find_element(By.ID, "id_password2").click()
        self.cleaner.find_element(By.ID, "id_password2").send_keys("admin12345678")
        self.cleaner.find_element(By.ID, "id_email").click()
        self.cleaner.find_element(By.ID, "id_email").send_keys(email)
        self.cleaner.find_element(By.ID, "id_first_name").click()
        self.cleaner.find_element(By.ID, "id_first_name").send_keys("Jhon")
        self.cleaner.find_element(By.ID, "id_last_name").click()
        self.cleaner.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.cleaner.find_element(By.CSS_SELECTOR, ".btn").click()
        self.cleaner.get("http://localhost:8000/authentication/login-view/")
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("admin12345678")
        self.cleaner.find_element(By.ID, "id_password1").send_keys(Keys.ENTER)
        self.assertTrue(self.cleaner.current_url == "http://localhost:8000/")


class TestLoginNegative(TestCase):
  
  
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.cleaner = webdriver.Chrome(options=options)


        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()

        self.cleaner.quit()

        self.base.tearDown()
  
    def test_testlogin_negative(self):
        
        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = "userLoginError"+str(delta.total_seconds())

        email = "testEmailLoginError"+str(delta.total_seconds())+"@gm.com"

        self.cleaner.get("http://localhost:8000/authentication/register/")
        self.cleaner.set_window_size(917, 1023)
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("admin123456789")
        self.cleaner.find_element(By.ID, "id_password2").click()
        self.cleaner.find_element(By.ID, "id_password2").send_keys("admin123456789")
        self.cleaner.find_element(By.ID, "id_email").click()
        self.cleaner.find_element(By.ID, "id_email").send_keys(email)
        self.cleaner.find_element(By.ID, "id_first_name").click()
        self.cleaner.find_element(By.ID, "id_first_name").send_keys("Jhon")
        self.cleaner.find_element(By.ID, "id_last_name").click()
        self.cleaner.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.cleaner.find_element(By.CSS_SELECTOR, ".btn").click()
        self.cleaner.get("http://localhost:8000/authentication/login-view/")
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys(username)
        self.cleaner.find_element(By.ID, "id_password1").click()
        self.cleaner.find_element(By.ID, "id_password1").send_keys("admin12345678")
        self.cleaner.find_element(By.ID, "id_password1").send_keys(Keys.ENTER)
        self.assertTrue(self.cleaner.current_url == "http://localhost:8000/authentication/login-view/")
        self.assertTrue( self.cleaner.find_element(By.CSS_SELECTOR, ".alert").text == "Username and password do not match")





class TestPositiveCleans(TestCase):

    def test_positive_cleans(self):
        username = "antonio123456"
        pass1 = "admin00000"
        pass2 = "admin00000"
        email = "antonio12346@gmail.com"
        first_name = "Jhon"
        last_name = "Doe"

        cleaner = CustomUserCreationForm()

        self.assertFalse(cleaner.clean_password2(pass1, pass2))
        self.assertFalse(cleaner.username_clean_lenght(username))
        self.assertFalse(cleaner.username_clean_exits(username))
        self.assertFalse(cleaner.username_clean_pattern(username))
        self.assertFalse(cleaner.email_clean(email))
        self.assertFalse(cleaner.clean_password_lenght(pass1))
        self.assertFalse(cleaner.clean_password_commonly(pass1))
        self.assertFalse(cleaner.clean_password_too_similar(pass1, username, first_name, last_name))
        self.assertFalse(cleaner.clean_password_numeric(pass1))


class TestNegativeCleans(TestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter12345')
        u.set_password('123')
        u.email = "voter12345@gmail.com"
        u.save()

    def tearDown(self):
        self.client = None


    def test_negative_cleans(self):
        cleaner = CustomUserCreationForm()

        self.assertTrue(cleaner.clean_password2("admin00000", "admin1111111"))
        self.assertTrue(cleaner.username_clean_lenght("Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis pa"))
        self.assertTrue(cleaner.username_clean_exits("voter12345"))
        self.assertTrue(cleaner.username_clean_pattern("user~$"))
        self.assertTrue(cleaner.email_clean("voter12345@gmail.com"))
        self.assertTrue(cleaner.clean_password_lenght("testprq"))
        self.assertTrue(cleaner.clean_password_commonly("qwertyui"))
        self.assertTrue(cleaner.clean_password_too_similar("antonio2", "antonio2", "antonio", "Doe"))
        self.assertTrue(cleaner.clean_password_numeric("1234567890123"))
        