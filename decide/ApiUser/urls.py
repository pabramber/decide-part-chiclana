from django.urls import path
from .views import UserListViews
urlpatterns = [
    path('user/', UserListViews.as_view(), name='user_list')
]
