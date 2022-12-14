import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
import itertools


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

    def get(self, request, *args, **kwargs):
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt', 'postproc_type', 'number_seats']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        end_date = request.data.get('end_date')
        start_date = request.data.get('start_date')
        future_start = request.data.get('future_start')
        future_stop = request.data.get('future_stop')
        postproc_type = request.data.get('postproc_type')
        number_seats = request.data.get('number_seats')
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                end_date = end_date,
                start_date = start_date,
                future_start = future_start,
                future_stop = future_stop,
                question=question,
                postproc_type=postproc_type,
                number_seats=number_seats)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)

    
class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        elif action == 'save':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.tally:
                msg = 'Voting has not being tallied' 
                st = status.HTTP_400_BAD_REQUEST
            else: 
                voting.save_file()
                msg = 'Saved voting file'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)

def create_yes_no_question(self):
    options = QuestionOption.objects.all().filter(question=self)
    for o in options:
        o.delete()
    option_yes = QuestionOption(option='S??', number=1, question=self)
    option_yes.save()
    option_no = QuestionOption(option='No', number=2, question=self)
    option_no.save()

def create_ranked_question(self):
    try:
        options = QuestionOption.objects.all().filter(question=self)
        num_options = len(options)
        list_options = []

        for o in options:
            list_options.append(o.option + ', ')

        permutation = itertools.permutations(list_options, num_options)
                
        for iter in permutation:
            option = QuestionOption(option=''.join(iter), question=self)
            option.save()

        for o in options:
            o.delete()

        self.create_ordination = False
        self.save()
        
    except:
        pass

def create_score_question(self):
    try:
        options = QuestionOption.objects.all().filter(question=self)
        list_options = [str(o.option) for o in options]

        for i in range(0, 11):
            if str(i) in list_options:
                continue
            else:
                option = QuestionOption(option=str(i), question=self)
                option.save()

    except:
        pass