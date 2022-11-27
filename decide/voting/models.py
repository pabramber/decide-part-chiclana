from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Vote
from base import mods
from base.models import Auth, Key
from postproc.models import PostprocTypeEnum


class Question(models.Model):
    desc = models.TextField()
    TYPES = [
            ('O', 'Options'),
            ('S', 'Score'),
            ('P', 'Preference'),
            ]
    tipo = models.CharField(max_length=1, choices=TYPES, default='O')  
    yes_no_question = models.BooleanField(verbose_name='Yes/No question', default=False)
    create_ordination = models.BooleanField(verbose_name='Create ordination', default=False)

    def save(self):
        super().save()
        if self.yes_no_question:
            import voting.views # Importo aquí porque si lo hago arriba da error por importacion circular
            voting.views.create_yes_no_question(self)
        elif self.tipo == 'P' and self.create_ordination:
            import voting.views
            voting.views.create_preference_question(self)

    def __str__(self):
        return self.desc
@receiver(post_save, sender=Question)
def my_handler(sender, instance, **kwargs):
    if instance.tipo == 'S':
        instance.options.all().delete()
        instance.options.create(option='1')
        instance.options.create(option='2')
        instance.options.create(option='3')
        instance.options.create(option='4')
        instance.options.create(option='5')
        instance.options.create(option='6')
        instance.options.create(option='7')
        instance.options.create(option='8')
        instance.options.create(option='9')
        instance.options.create(option='10')


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self, *args, **kwargs):
        if self.question.yes_no_question:
            if not self.option == 'Sí' and not self.option == 'No':
                return ""
        else:
            if not self.number:
                self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

    voting_types = (
        ('CV', 'CLASSIC VOTING'),
        ('PV', 'PREFERENCE VOTING'),
        ('BV', 'BINARY VOTING'),
        ('SV', 'SCORE VOTING'),)

    voting_type = models.CharField(max_length=2, choices=voting_types, default='CV')

    postproc_type = models.CharField(max_length=255, choices=PostprocTypeEnum.choices(), default='IDENTITY')
    number_seats = models.PositiveIntegerField(default=1)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })
        
        data = { 'type': self.postproc_type, 'seats': self.number_seats, 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
