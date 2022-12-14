from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ReporteAutorExcel


urlpatterns = [
    path('create', views.createCensus, name='census_create'),
    path('details<int:voting_id>', views.CensusDetail.as_view(), name='census_detail'),
    path('detalles/',views.GetId),
    path('delete/',views.deleteCensus),
    path('',views.hello, name="hello"),
    path('importer/', views.importer, name='importer'),
    path('succeed',views.censusCreatedSucced),
    path('deleted',views.censusDeletedSucced),
    path('filter/', views.filter, name='filter'),
    path('filter-votingID/', views.FilterVotingID.as_view(), name='filter_votingID'),
    path('filter-voterID/', views.FilterVoterID.as_view(), name='filter_voterID'),
    path('filter-name/', views.FilterName.as_view(), name='filter_name'),
    path('filter-surname/', views.FilterSurname.as_view(), name='filter_surname'),
    path('filter-city/', views.FilterCity.as_view(), name='filter_city'),
    path('filter-community/', views.FilterCommunity.as_view(), name='filter_community'),
    path('filter-gender/', views.FilterGender.as_view(), name='filter_gender'),
    path('filter-bornYear/', views.FilterBornYear.as_view(), name='filter_bornYear'),
    path('filter-civilstate/', views.FilterCivilState.as_view(), name='filter_civil_state'),
    path('filter-sexuality/', views.FilterSexuality.as_view(), name='filter_sexuality'),
    path('filter-works/', views.FilterWorks.as_view(), name='filter_works'),
    url(r'^reporte/', login_required(ReporteAutorExcel.as_view()), name = "reporte"),


]
