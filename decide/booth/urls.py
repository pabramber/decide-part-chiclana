from django.urls import path
from .views import BoothView, get_votings


urlpatterns = [
    path('', get_votings),
    path('<int:voting_id>/', BoothView.as_view()),
]