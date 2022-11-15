from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_200_OK,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
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
            'username':('Userame'),
            'password1':('Password'),
            'password2':('Repeat the password'),
            'email':('Email'),
            'first_name':('First Name'),
            'last_name':('Last Name')
        }
  
    def username_clean(self, username):  
        username = username.lower()  

        new = User.objects.filter(username = username)  
        if new.count():  
            return True

        if len(username) > 150:
            return True
        
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

class RegisterView(CreateView):
    template_name = "authentication/authentication.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    model = User

    def get_form(self, form_class=None):
        form = super(RegisterView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2'}) 
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2'}) 
        form.fields['first_name'].widget = forms.TextInput(attrs={'class':'form-control mb-2'}) 
        form.fields['last_name'].widget = forms.TextInput(attrs={'class':'form-control mb-2'}) 
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2'}) 

        return form

    def get_success_url(self):
        return reverse_lazy("/authentication/login")

    def post(self, request):
        values = request.POST   

        
        username = values['username']
        pass1 = values['password1']
        pass2 = values['password2']
        email = values['email']
        ver = CustomUserCreationForm()

        if(ver.clean_password2(pass1, pass2)):
            return HttpResponse("Both passwords must be the same", status=HTTP_400_BAD_REQUEST)
        if(ver.username_clean(username)):
            return HttpResponse("This username has already taken by other user or the username is not like the template", status=HTTP_400_BAD_REQUEST)
        if(ver.email_clean(email)):
            return HttpResponse("This email has already taken by other user", status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.first_name = values['first_name']
            user.last_name = values['last_name']
            user.email = email
            user.set_password(pass1)
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
        if user is not None:
            login(request, user)
            print("authenticate")
        else:
            print("usuario no autenticado")
            return HttpResponse("Username and password do not match", status=HTTP_400_BAD_REQUEST)

        return redirect("/")

