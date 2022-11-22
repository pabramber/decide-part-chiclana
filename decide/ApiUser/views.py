from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

# Create your views here.
from .serializers import *


class UserListViews(APIView):
    """
    API endpoint that allows users to be viewed or created.
    """
    serializer_class = UserSerializer
    
    def get(self,request):
       """
        This list all users of Decide application.
       """
       userList = User.objects.all().values()
       return Response({"Message": "New user added", "user":userList})

    def post(self, request):
        """
            This create a new user.
            user: [ {"username": str, "first_name": str, "last_name": str, "password": str,
            "email": str,"is_staff": bool} ]
        """
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
    """
    API endpoint that allows users to be viewed or updated by id.
    """
    serializer_class = UserSerializer
    """
            This update a user.
            user: [ {"username": str, "first_name": str, "last_name": str, "password": str,
            "email": str,"is_staff": bool} ]
    """
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
    
    def get(self,request, id):
        """
            Success: This shows the details of the user.
            Fail: This shows a status 204 not found.
        """
        print("request data in get one user is: ", request.data)
        users = list(User.objects.filter(id=id).values())
        
        if len(users)>0:
            user = users[0]
            return Response({"Message": "This are the details of the searched user:",
            "user":user})
        else:
            return Response({"Message": "The user  can not be found in Decide application."}
            ,status=ST_204)

class UserStaffView(APIView):
    """
    API endpoint that allows knows if a user is a staff member or not by id.

    Success: This shows if the user is staff.
    Fail: This shows a status 204 not found.
    """
    def get(self,request, id):
        print("request data in is_staff user is: ", request.data)
        users = list(User.objects.filter(id=id).values())
        if len(users)>0:
            user = users[0]
            is_staff = user.get('is_staff')
            username = (user.get('username')).upper()
            
            if(is_staff):
                return Response({"Message": "The user "+username+" is a staff member"})
            else:
                return Response({"Message": "The user "+username+" is not a staff member"})
        else:
            return Response({"Message": "The user  can not be found in Decide application."}
            ,status=ST_204)
            
       

        
