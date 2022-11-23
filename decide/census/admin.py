from django.contrib import admin

from import_export.admin import ImportExportModelAdmin


from django.core.mail import send_mail
from .models import Census
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from voting.models import Voting
from django.utils.html import strip_tags


def enviar_mail(modeladmin, request, queryset):
    for c in queryset.all():
        user_id = c.voter_id
        voting_id = c.voting_id
        user = User.objects.get(id = user_id)
        voting = Voting.objects.get(id = voting_id)
       
        mensaje= render_to_string("emails/notificacion.html",{
            "nombre": user.username,
            "email": user.email,
            "description": voting.desc,
            "fecha_inicio": voting.start_date,
            "question": voting.question,
            "tipo": voting.question.tipo,
            "nombre_votacion": voting.name,
            "votacion_id": voting_id
            


        })


@admin.register(Census)
class CensusAdmin(ImportExportModelAdmin):
    list_display = ('voting_id','voter_id','name','surname','city',
                    'a_community','gender','born_year','civil_state',
                    'sexuality','works')

        asunto = "Ya puede realizar su voto en la aplicacion Decide"
        mensaje_texto = strip_tags(mensaje)

        from_mail = "pgpig3.3@gmail.com"
        to_email = user.email
        send_mail(asunto,mensaje,from_mail,[to_email], html_message=mensaje)

class CensusAdmin(admin.ModelAdmin):
    actions = [enviar_mail]
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )
    search_fields = ('voter_id', )
    

     



admin.site.register(Census, CensusAdmin)

