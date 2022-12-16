from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting

from .filters import StartedFilter


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)

def save(ModelAdmin, request ,queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        v.save_file()

save.short_description = 'Save voting file'

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    list_display = ('image_tag',)
    readonly_fields = ('image_tag',)



class QuestionAdmin(admin.ModelAdmin):
    list_display = ('desc', 'type')
    inlines = [QuestionOptionInline]
    list_display = ('desc','type')

class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date','future_start', 'future_stop')
    readonly_fields = ('start_date','end_date','pub_key',
                       'tally', 'postproc', 'file')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally, save ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
