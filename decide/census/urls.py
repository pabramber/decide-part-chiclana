from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('filter', views.FiltroVotante.as_view(), name='census_filtros'),
    path('filtros/', views.filtros),
]
