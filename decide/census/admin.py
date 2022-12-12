from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Census

@admin.register(Census)
class CensusAdmin(ImportExportModelAdmin):
    list_display = ('voting_id','voter_id','name','surname','city',
                    'a_community','gender','born_year','civil_state',
                    'sexuality','works')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )


