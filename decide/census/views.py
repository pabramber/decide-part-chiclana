from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .resources import CensusResource
from tablib import Dataset
from .models import Census
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render


def filter(request):
    censo = Census.objects.all()
    return render(request, 'filterCensus.html', {'census' : censo})

class FilterVotingID(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('i')
        return Census.objects.filter(voting_id__icontains=query).order_by('-voting_id')

class FilterVoterID(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('i')
        return Census.objects.filter(voting_id__icontains=query).order_by('-voter_id')

class FilterName(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Census.objects.filter(name__icontains=query).order_by('-name')

class FilterSurname(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('i')
        return Census.objects.filter(surname__icontains=query).order_by('-surname')

class FilterCity(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(city__icontains=query).order_by('-city')

class FilterCommunity(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(a_community__icontains=query).order_by('-a_community')

class FilterGender(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(gender__icontains=query).order_by('-gender')

class FilterBornYear(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(born_year__icontains=query).order_by('-born_year')

class FilterCivilState(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(civil_state__icontains=query).order_by('-civil_state')

class FilterSexuality(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(sexuality__icontains=query).order_by('-sexuality')

class FilterWorks(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(works__icontains=query).order_by('-works')
    

def importer(request):
    if request.method == 'POST':
        census_resource = CensusResource()
        dataset = Dataset()
        new_census = request.FILES['myfile']

        if not new_census.name.endswith('xlsx'):
            messages.info(request, 'formato incorrecto, debe ser .xslx')
            return render(request, 'importer.html')

        imported_data = dataset.load(new_census.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
            value = Census(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11]
                    ) 
            value.save()
        
        #result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        #if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'importer.html')



class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
                
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})

    

class CensusDetail(generics.RetrieveDestroyAPIView):


    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')


def GetId(request):
    id = request.GET['id']
    census = Census.objects.filter(voting_id=int(id))
    return render(request,"census_details.html",{'census':census})

def hello(request):
    return render(request,'census.html')



