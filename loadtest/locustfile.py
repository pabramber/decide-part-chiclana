import json

from random import choice

from datetime import datetime
from bs4 import BeautifulSoup

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)

HOST = "http://localhost:8000"
VOTING = 1


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))


class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/store/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING
        }), headers=headers)

    def on_quit(self):
        self.voter = None


class DefRegister(TaskSet):

    @task
    def register(self):
        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = 'userLocust'+str(delta.total_seconds())
        pwd = 'contrasenia12345'
        email = 'test'+str(delta.total_seconds())+'@gm.com'
        first_name = 'Jhon'
        last_name = 'Doe'

        html = self.client.get("/authentication/register/").text
        soup = BeautifulSoup(html, 'html.parser')
        csrf_field = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        csrf_value = csrf_field['value']

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            "X-CSRFToken": csrf_value
        }
    
        with self.client.post("/authentication/register/", {
                'username': [username],
                'password1': [pwd],
                'password2': [pwd],
                'email': [email],
                'first_name': [first_name],
                'last_name': [last_name],
                'csrfmiddlewaretoken': [csrf_value],
            }, headers=headers, catch_response=True) as response:

            current_url = self.client.base_url

            if response.status_code == 404 and current_url == "http://localhost:8000":
                response.success()


class DefLogin(TaskSet):

    @task
    def login(self):
        dt = datetime.now()
        epoch_time = datetime(1970, 1, 1)
        delta = (dt - epoch_time)
        
        username = 'userLocust'+str(delta.total_seconds())
        pwd = 'contrasenia12345'
        email = 'test'+str(delta.total_seconds())+'@gm.com'
        first_name = 'Jhon'
        last_name = 'Doe'

        html = self.client.get("/authentication/register/").text
        soup = BeautifulSoup(html, 'html.parser')
        csrf_field = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        csrf_value = csrf_field['value']

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            "X-CSRFToken": csrf_value
        }
    
        with self.client.post("/authentication/register/", {
                'username': [username],
                'password1': [pwd],
                'password2': [pwd],
                'email': [email],
                'first_name': [first_name],
                'last_name': [last_name],
                'csrfmiddlewaretoken': [csrf_value],
            }, headers=headers, catch_response=True) as response:

            html2 = self.client.get("/authentication/login-view/").text
            soup2 = BeautifulSoup(html2, 'html.parser')
            csrf_field2 = soup2.find('input', {'name': 'csrfmiddlewaretoken'})
            csrf_value2 = csrf_field2['value']

            with self.client.post("/authentication/login-view/", {
                'username': [username],
                'password1': [pwd],
                'csrfmiddlewaretoken': [csrf_value2],
            }, headers=headers, catch_response=True) as response2:

                current_url2 = self.client.base_url

                response.success()
                
                if response2.status_code == 404 and current_url2 == "http://localhost:8000":
                    response2.success()



class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)



class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)


class Register(HttpUser):
    host =HOST
    tasks = [DefRegister]
    wait_time = between(3, 5)

class Login(HttpUser):
    host =HOST
    tasks = [DefLogin]
    wait_time = between(3, 5)
