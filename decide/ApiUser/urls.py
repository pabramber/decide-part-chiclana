from django.urls import path
from .views import UserListViews, UserDetailViews
urlpatterns = [
    path('user/list', UserListViews.as_view(), name='user_list'),
    path('user/<int:id>', UserDetailViews.as_view(), name='user_update')

]
