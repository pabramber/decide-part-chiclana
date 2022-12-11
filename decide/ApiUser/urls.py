from django.urls import path
from .views import UserListViews, UserDetailViews,UserStaffView, UserExistsView
urlpatterns = [
    path('user/list', UserListViews.as_view(), name='user_list'),
    path('user/<int:id>', UserDetailViews.as_view(), name='user_update'),
    path('user/staff/<int:id>', UserStaffView.as_view(), name='user_is_staff'),
    path('user/exists/<str:username>', UserExistsView.as_view(), name='user_exists')

]
