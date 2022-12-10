

from django import forms
from .models import Census


class CreationCensusForm(forms.Form):
    voting_id = forms.IntegerField()
    voter_id = forms.IntegerField()
    name = forms.CharField()
    surname = forms.CharField()
    city = forms.CharField()
    a_community = forms.CharField()
    gender = forms.CharField()
    born_year = forms.IntegerField()
    civil_state = forms.CharField()
    sexuality = forms.CharField()
    works = forms.IntegerField()


    class Meta: 
        model = Census
        fields = (
            'voting_id',
            'voter_id',
            'name',
            'surname',
            'city',
            'a_community',
            'gender',
            'born_year',
            'civil_state',
            'sexuality',
            'works'
        )
    def save (self, commit = True):
        census = super(CreationCensusForm, self).save(commit = False)
        census.voting_id = self.cleaned_data['voting_id']
        census.voter_id = self.cleaned_data['voter_id']
        census.name = self.cleaned_data['name']
        census.surname= self.cleaned_data['surname']
        census.city = self.cleaned_data['city']
        census.a_community = self.cleaned_data['a_community']
        census.gender = self.cleaned_data['gender']
        census.born_year = self.cleaned_data['born_year']
        census.civil_state = self.cleaned_data['civil_state']
        census.sexuality = self.cleaned_data['sexuality']
        census.works = self.cleaned_data['works']

        if commit : 
            census.save()
        return census





