from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.
from django.http import JsonResponse
class UserListViews(APIView):
    def get(self,request):
       userList = User.objects.all()
       return JsonResponse(list(userList.values()), safe=False)


