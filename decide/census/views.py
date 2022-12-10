from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
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
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CreationCensusForm


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
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')




def GetId(request):
    id = request.GET['id']
    census = Census.objects.filter(voting_id=int(id))
    return render(request,"census_details.html",{'census':census})

def hello(request):
    return render(request,'census.html')


def createCensus(request): 
    if request.method == 'GET':
        return render(request, 'census_create.html',{'form': CreationCensusForm})
    else: 
        if request.method == 'POST':
            try: 
                census = Census.objects.create(voting_id = request.POST['voting_id'],voter_id = request.POST['voter_id'],
                name = request.POST['name'],surname= request.POST['surname'],city = request.POST['city'],a_community = request.POST['a_community'],
                gender = request.POST['gender'],born_year = request.POST['born_year'],civil_state = request.POST['civil_state'],
                sexuality = request.POST['sexuality'],works = request.POST['works'])
                census.save()
                return HttpResponse('The census was created correctly')
            except: 
                return render(request,'census_create.html',{'form': CreationCensusForm, "error": 'Census already exist'})
        return  render(request,'census_create.html',{'form': CreationCensusForm})
        
def deleteCensus(request):
    Voterid = request.GET['Voterid']
    Votingid = request.GET['Votingid']
    census = Census.objects.filter(voting_id=int(Votingid),voter_id = int(Voterid))
    if len(census) == 0: 
        return HttpResponse('There is not Census')
    census.delete()
    return HttpResponse('The census was deleted correctly')
    




    return None