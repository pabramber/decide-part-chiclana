from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ReporteAutorExcel



urlpatterns = [
    path('create', views.CensusCreate.as_view(), name='census_create'),
    path('details<int:voting_id>', views.CensusDetail.as_view(), name='census_detail'),
    path('detalles/',views.GetId),
    path('',views.hello, name="hello"),
    path('importer/', views.importer, name='importer'),
    path('lista_censo/', views.home, name = 'lista_censo'),
    url(r'^reporte/', login_required(ReporteAutorExcel.as_view()), name = "reporte"),
]
