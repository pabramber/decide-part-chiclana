import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect

from base import mods
from census.models import Census
from voting.models import Voting
from django.contrib.auth.models import User


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

def get_votings(request):

    if request.user.id is None:
            messages.error(request, 'Log in')
            return redirect('login')

    else:  
        census = Census.objects.filter(voter_id=request.user.id)
        votings = []

        for c in census:
            voting = Voting.objects.get(id=c.voting_id)
            votings.append(voting)

        print(len(votings))
    return render(request, 'booth/votingsList.html', {'votings': votings})
