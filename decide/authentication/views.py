from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_200_OK,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from django.http import HttpRequest, QueryDict
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from .serializers import UserSerializer
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form 
import re
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.shortcuts import render
from census.models import Census
from voting.models import Voting


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})



class CustomUserCreationForm(UserCreationForm):  

    class Meta(UserCreationForm.Meta):
        model = User
        fields= (
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name'
        )

        labels = {
            'username':('Username'),
            'password1':('Password'),
            'password2':('Repeat the password'),
            'email':('Email'),
            'first_name':('First Name'),
            'last_name':('Last Name')
        }
  
    def username_clean_lenght(self, username):  
        username = username.lower()  

        if len(username) > 150:
            return True
        else:
            return False
        

    def username_clean_exits(self, username):
        username = username.lower()

        new = User.objects.filter(username = username)  
        if new.count():  
            return True
        else:
            return False

    def username_clean_pattern(self, username):
        username = username.lower()

        username_val_regex = re.search("[^\w@.\-_+]", username)
        if(username_val_regex != None):
            return True
        return False
  
    def email_clean(self,email):  
        email = email.lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            return True
        return False
  
    def clean_password2(self, password1, password2):  
        if password1 and password2 and password1 != password2:  
            return True
        return False
    
    def clean_password_lenght(self, password1):
        if len(password1)<8:
            return True
        else:
            return False

    def clean_password_commonly(self, password1):
        commonly_passwords = ['12345678 ', '11111111', '00000000', 'password', 'password0', 'password1', 'decide', 'decide password', 'password decide', '01234567', 
        '2345678', 'qwertyui', 'asdfghjk', 'zxcvbnm', 'password123', 'password12', 'password1234', 'iloveyou', 'welcome', '1q2w3e4r', 'adminadmin', 'admin123', '1234567890',
        '0987654321', '87654321', 'google12', 'google00', 'monkey', 'dragon']

        ret = False
        for common_password in commonly_passwords:

            if (password1==common_password):
                ret = True
                break
        
        return ret

    def clean_password_too_similar(self, password, username, first_name, last_name):
        if (password.__contains__(username) | password.__contains__(first_name) | password.__contains__(last_name)):
            return True
            
        else:
            return False

    def clean_password_numeric(self, password):
        if (password.isnumeric()):
            return True
        else:
            return False


class RegisterView(CreateView):
    template_name = "authentication/authentication.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    model = User

    def get_form(self, form_class=None):
        form = super(RegisterView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'150 characters or fewer. Letters, digits and @/./+/-/_ only.'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'8 characters or more. Can\'t be too similar to your personal data or a commonly password or entirely numeric'}) 
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Must be the same as the previous password'}) 
        form.fields['first_name'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Jhon'}) 
        form.fields['last_name'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Doe'}) 
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Insert an email like this: jhondoe@example.com'}) 

        return form

    def get_success_url(self):
        return reverse_lazy("/authentication/login")

    def post(self, request):
        values = request.POST   

        username = values['username']
        pass1 = values['password1']
        pass2 = values['password2']
        email = values['email']
        first_name = values['first_name']
        last_name = values['last_name']
        ver = CustomUserCreationForm()

        errors = []


        if(ver.clean_password2(pass1, pass2)):
            errors.append("Both passwords must be the same")

        if(ver.username_clean_lenght(username)):
            errors.append("This username is higher 150 characters")
           
        if(ver.username_clean_exits(username)):
            errors.append("This username has already taken by other user")

        if(ver.username_clean_pattern(username)):
            errors.append("This username is not like the template")

        if(ver.email_clean(email)):
            errors.append("This email has already taken by other user")
            
        if(ver.clean_password_lenght(pass1)):
            errors.append("This password must contain at least 8 characters")

        if(ver.clean_password_commonly(pass1)):
            errors.append("This password is a commonly password")

        if(ver.clean_password_too_similar(pass1, username, first_name, last_name)):
            errors.append("This password is too similar to your personal data")

        if(ver.clean_password_numeric(pass1)):
            errors.append("This password is entirely numeric")


        if (len(errors)>0):
            template = loader.get_template("authentication/authentication.html")
            context = {"errors":errors}

            return HttpResponse(template.render(context, request))
        else:
            try:
                user = User(username=username)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.set_password(pass1)

                email=EmailMessage("Message from the app Decide", 

                "The user with name {} and email {} has registered in the app Decide".format(user.first_name,user.email), 

                "",[user.email], reply_to=[email])

                email.send()

                user.save()
                token, _ = Token.objects.get_or_create(user=user)

            except IntegrityError:
                return HttpResponse("Integrity Error raised", status=HTTP_400_BAD_REQUEST)

            return redirect("/")



    
class LoginView(CreateView):

    template_name = "authentication/login.html"
    form_class = CustomUserCreationForm
    model = User

    def post(self, request):
        values = request.POST   

        username = values['username']
        pass1 = values['password1']
        
        user = authenticate(request, username=username, password=pass1)
        userObject = User.objects.get(username=username)

        response = redirect("/")

        if user is not None:

            email=user.email
            
            login(request, user)

            email=EmailMessage("Message from the app Decide", 

            "The user with email {} has logged in the app Decide".format(email), 

            "",[email], reply_to=[email])

            email.send()
            token, created = Token.objects.get_or_create(user=userObject)
            response.set_cookie(key='token', value=token)
        else:
            errors = ["Username and password do not match"]
            template = loader.get_template("authentication/authentication.html")
            context = {"errors":errors}

            return HttpResponse(template.render(context, request))

        


        return response


    @staticmethod     
    def authenticated(request):
        return render(request, 'authentication/authenticated.html', {
                'username' : request.user
            })



class RegisterViewAPI(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)


def main(request):
    template = loader.get_template("authentication/decide.html")
    context = {}
    authenticated = False
    votings=[]
    if request.user.is_authenticated == True:
        authenticated = True
        context['username'] = request.user.username
        census = Census.objects.filter(voter_id=request.user.id)
        for c in census:
            voting_id = c.voting_id

            voting = Voting.objects.get(id = voting_id)
            
            if voting is not None and voting.start_date is not None and voting.end_date is None:
                votings.append(voting) 

    context['authenticated'] = authenticated
    context['votings'] = votings

    return HttpResponse(template.render(context, request))


def logout_view(request):
    response = redirect("/")
    if request.user.is_authenticated == True:
        logout(request)
        response.delete_cookie('token')
        response.delete_cookie('decide')
    return response


