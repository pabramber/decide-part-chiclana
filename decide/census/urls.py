from django.urls import path, include
from . import views


urlpatterns = [
    path('create', views.createCensus, name='census_create'),
    path('details<int:voting_id>', views.CensusDetail.as_view(), name='census_detail'),
    path('detalles/',views.GetId),
    path('delete/',views.deleteCensus),
    path('',views.hello, name="hello"),
    path('importer/', views.importer, name='importer'),
]
