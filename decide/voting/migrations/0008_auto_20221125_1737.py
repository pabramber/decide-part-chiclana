# Generated by Django 2.0 on 2022-11-25 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_voting_voting_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='future_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='voting',
            name='future_stop',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]