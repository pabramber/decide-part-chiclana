# Generated by Django 2.0 on 2022-12-09 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0014_auto_20221208_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='postproc_type',
            field=models.CharField(choices=[('IDENTITY', 'IDENTITY'), ('DHONDT', 'DHONDT'), ('DROOP', 'DROOP'), ('HARE', 'HARE')], default='IDENTITY', max_length=255),
        ),
    ]