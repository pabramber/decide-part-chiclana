from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Vote
from base import mods
from base.models import Auth, Key
from django.utils import timezone
from postproc.models import PostprocTypeEnum
from datetime import datetime
from django.core.validators import URLValidator
import requests
from io import StringIO
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

class Question(models.Model):
    desc = models.TextField()
    TYPES = [
            ('C', 'Classic question'),
            ('S', 'Score question'),
            ('R', 'Ranked question'),
            ('B', 'Yes/No question'),
            ('I', 'Image'),
            ]
    type = models.CharField(max_length=1, choices=TYPES, default='C')  
    create_ordination = models.BooleanField(verbose_name='Create ordination', default=False)

    def save(self):
        super().save()
        if self.type == 'B':
            import voting.views # Importo aquí porque si lo hago arriba da error por importacion circular
            voting.views.create_yes_no_question(self)
        elif self.type == 'R' and self.create_ordination:
            import voting.views
            voting.views.create_ranked_question(self)
        elif self.type == 'S':
            import voting.views
            voting.views.create_score_question(self)

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def clean(self):
        if self.question.type == 'I':
            validator = URLValidator()
            validator(self.option)
            image_formats = ("image/png", "image/jpeg", "image/jpg")
            r = requests.get(self.option)
            if r.headers["content-type"] not in image_formats:
                raise ValidationError("Url does not contain a compatible image")

    def save(self, *args, **kwargs):
        if self.question.type == 'B':
            if not self.option == 'Sí' and not self.option == 'No':
                return ""
        else:
            if not self.number:
                self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)
    
    def image_tag(self):
        from django.utils.html import escape
        if self.question.type == 'I':
            return mark_safe(u'<img src="%s" width="150" height="150" />' % escape(self.option))
        else:
            return ""
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

    postproc_type = models.CharField(max_length=255, choices=PostprocTypeEnum.choices(), default='IDENTITY')
    number_seats = models.PositiveIntegerField(default=1)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    future_start = models.DateTimeField(blank=True, null=True)
    future_stop = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    file = models.FileField(blank=True)

    def read_file(self):
        import warnings
        warnings.filterwarnings("ignore")
        text_buffer = self.file.open("rb")
        auths = []
        voting_desc = ""
        voting_name = ""
        question_desc = ""
        question_type = ""
        options = []
        future_start = None
        future_stop = None
        voting:Voting = None
        question:Question = None
        lines = text_buffer.readlines()
        for line in lines:
            line = line.decode("utf-8")
            if line.find("auths") != -1:
                auths_list = line.split(":",1)[1].replace("[(","").replace(")]","").strip().split("),(")
                for auth_str in auths_list:
                    try:
                        auth_split = auth_str.split(",")
                        auth = Auth(name=auth_split[0].strip(), url=auth_split[1].strip())
                        auths.append(auth)
                    except:
                        raise ValidationError("You need to add a valid auth")
            if line.find("question_desc") != -1:
                question_desc = line.split(":",1)[1].strip()
            if line.find("voting_desc") != -1:
                voting_desc = line.split(":",1)[1].strip()
            if line.find("options") != -1:
                options_str_list = line.split(":",1)[1].replace("[(","").replace(")]","").strip().split("),(")
                for option_str in options_str_list:
                    option = option_str.split(",")
                    options.append(option)
            if line.find("voting_name") != -1:
                voting_name = line.split(":",1)[1].strip()
            if line.find("question_type") != -1:
                question_type = line.split(":",1)[1].strip()
            if line.find("future_start") != -1:
                future_start_str = line.split(":",1)[1].strip()
                future_start = datetime.strptime(future_start_str, "%Y-%m-%d %H:%M:%S")
            if line.find("future_stop") != -1:
                future_end_str = line.split(":",1)[1]
                future_stop = datetime.strptime(future_start_str, "%Y-%m-%d %H:%M:%S")
        text_buffer.close
        question = Question(desc=question_desc,type=question_type)
        try:
            question.full_clean()
            question.save()
        except:
            raise ValidationError("You need to add a question")
        
        for option in options:
            new_option = QuestionOption(question=question, number=int(option[0]), option=option[1])
            new_option.save()
        self.question = question
        self.desc = voting_desc
        self.name = voting_name
        if self.name == "":
            raise ValidationError("You need to add a name")
        self.future_start=future_start
        self.future_stop = future_stop
        self.save()
        for auth in auths:
            try:
                auth.save()
                auth.full_clean()
                self.auths.add(auth)
            except:
                raise ValidationError("You need to add a valid auth")
        

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
                'votes': votes,
                'borda': '',
            })
        
        data = { 'type': self.postproc_type, 'seats': self.number_seats, 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def save_file(self):
        if self.postproc:
            file_name = "[" + str(self.id) + "]" + self.name + ".txt"
            path = "voting/files/" + file_name
            file = open(path, "w")
            file.write("Id: " + str(self.id) + "\n")
            file.write("Nombre: " + self.name + "\n")
            file.write("Tipo de votación: " + self.question.type+ "\n")
            if self.desc:
                file.write("Descripción: " + self.desc + "\n")
            file.write("Fecha de inicio: " + self.start_date.strftime('%d/%m/%y %H:%M:%S') + "\n")
            file.write("Fecha de fin: " + self.end_date.strftime('%d/%m/%y %H:%M:%S') + "\n\n")
            file.write("Pregunta: " + str(self.question) + "\n")
            file.write("Resultado: \n")
            for opt in self.postproc:
                file.write("    - Opción: " + str(opt.get('option')))
                file.write("    Puntuación: " + str(opt.get('postproc')))
                file.write("    Votos: " + str(opt.get('votes')) + "\n")
            file.close()
            self.file = path
            self.save()    
    
        

    def __str__(self):
        return self.name

class VotingFromFile(models.Model):
    voting = models.ForeignKey(Voting(), related_name='voting', on_delete=models.CASCADE, blank=True)
    file_voting = models.FileField()
    def clean(self):
        v = Voting(file=self.file_voting)
        v.read_file()
        self.voting = v

def update_votings():
    
    fecha_hora = timezone.now()
    votaciones = list(Voting.objects.all())
    try:
        for v in votaciones :
            if(v.future_start <= fecha_hora):
                v.start_date = v.future_start
            if(v.future_stop <= fecha_hora):
                v.end_date = v.future_stop
            v.save()
    except:
        print("UPDATING PROCESS HAD AN ERROR")

