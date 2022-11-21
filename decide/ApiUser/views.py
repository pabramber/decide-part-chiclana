from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


# Create your views here.
from .serializers import *

class UserListViews(APIView):
   
    serializer_class = UserSerializer
    def get(self,request):
       userList = User.objects.all().values()
       return Response({"Message": "New user added", "user":userList})

    def post(self, request):
        print("request data is: ", request.data)
        serializer_obj = UserSerializer(data=request.data)
        if(serializer_obj.is_valid()):

            user = User(username=serializer_obj.data.get("username"))
            user.first_name = serializer_obj.data.get("first_name")
            user.last_name = serializer_obj.data.get("last_name")
            user.email = serializer_obj.data.get("email")
            user.is_staff = serializer_obj.data.get("is_staff")
            user.set_password(serializer_obj.data.get("password"))
            user.save()
            
        userResponse = User.objects.all().filter(username=request.data["username"]).values()
        return  Response({"Message": "New user added", "user":userResponse})


class UserDetailViews(APIView):
    serializer_class = UserSerializer

    def put(self, request, id):
        print("request data in put is: ", request.data)
        serializer_obj = UserSerializer(data=request.data)
        users = list(User.objects.filter(id=id).values())
        data = {}
        if len(users)>0:
            if(serializer_obj.is_valid()):

                user = User.objects.get(id=id)
                user.username = serializer_obj.data.get("username")
                user.first_name = serializer_obj.data.get("first_name")
                user.last_name = serializer_obj.data.get("last_name")
                user.is_staff = serializer_obj.data.get("is_staff")
                user.email = serializer_obj.data.get("email")
                user.password = serializer_obj.data.get("password")
                user.save()
                userResponse = User.objects.all().filter(username=request.data["username"]).values()
                data = {'Message': 'User updated.', 'user':userResponse}
            
        else:

            data = {'Message': 'User not found.'}
            
        return  Response(data)


        
