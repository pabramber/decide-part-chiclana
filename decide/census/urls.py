from django.urls import path, include
from . import views



urlpatterns = [
    path('create', views.CensusCreate.as_view(), name='census_create'),
    path('details<int:voting_id>', views.CensusDetail.as_view(), name='census_detail'),
    path('detalles/',views.GetId),
    path('',views.hello, name="hello"),
    path('importer/', views.importer, name='importer'),
    path('lista_censo/', views.home, name = 'lista_censo'),
]
