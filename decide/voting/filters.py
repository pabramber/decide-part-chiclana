from django.utils import timezone
from django.contrib.admin import SimpleListFilter


class StartedFilter(SimpleListFilter):
    title = 'started'
    parameter_name = 'started'

    def lookups(self, request, model_admin):
        return [
            ('NS', 'Not started'),
            ('R', 'Running'),
            ('F', 'Finished'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'NS':
            query =  queryset.filter(start_date__gt=timezone.now()) or \
                 queryset.exclude(start_date__isnull=False)
            return query
        if self.value() == 'R':
            return queryset.filter(start_date__lt=timezone.now()).exclude(end_date__lt=timezone.now())
        if self.value() == 'F':
            return queryset.filter(end_date__isnull = False)
        else:
            return queryset.all()
