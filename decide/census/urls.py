from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('filter/', views.filter, name='filter'),
    path('filter-votingID/', views.FilterVotingID.as_view(), name='filter_votingID'),
    path('filter-voterID/', views.FilterVoterID.as_view(), name='filter_voterID'),
    path('filter-name/', views.FilterName.as_view(), name='filter_name'),
    path('filter-surname/', views.FilterSurname.as_view(), name='filter_surname'),
    path('filter-city/', views.FilterCity.as_view(), name='filter_city'),
    path('filter-community/', views.FilterCommunity.as_view(), name='filter_community'),
    path('filter-gender/', views.FilterGender.as_view(), name='filter_gender'),

    path('filter-civilstate/', views.FilterCivilState.as_view(), name='filter_civil_state'),
    path('filter-sexuality/', views.FilterSexuality.as_view(), name='filter_sexuality'),

]
