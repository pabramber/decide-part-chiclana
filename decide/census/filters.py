import django_filters

from .models import Listing


class ListingFilter(django_filters.FilterSet):

    class Meta:
        model = Listing
        fields = {'voting_id': ['lt'], 'voter_id':['lt']}