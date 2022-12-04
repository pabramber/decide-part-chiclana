from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    name = models.CharField(max_length=40, null=True)
    surname = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=40, null=True)
    a_community = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10, null=True)
    born_year = models.PositiveIntegerField(null=True)
    civil_state = models.CharField(max_length=10, null=True)
    sexuality = models.CharField(max_length=20, null=True)
    works = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = (('voting_id','voter_id','name','surname','city',
                            'a_community','gender','born_year','civil_state',
                            'sexuality','works'),)


