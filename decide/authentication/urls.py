from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView, LoginView, RegisterViewAPI, logout_view


urlpatterns = [
    path('login-view/', LoginView.as_view(), name="login"), 
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('logout-view/', logout_view),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('authenticated/', LoginView.authenticated, name='authenticated'),
    path('register-api/', RegisterViewAPI.as_view()),

]
