# Generated by Django 2.0 on 2022-11-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='number_seats',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='voting',
            name='postproc_type',
            field=models.CharField(choices=[('IDENTITY', 'IDENTITY'), ('DHONDT', 'DHONDT')], default='IDENTITY', max_length=255),
        ),
    ]
