# Generated by Django 2.0 on 2022-11-28 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0010_voting_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='yes_no_question',
        ),
        migrations.AlterField(
            model_name='question',
            name='tipo',
            field=models.CharField(choices=[('O', 'Options'), ('S', 'Score'), ('P', 'Preference'), ('B', 'Yes/No question')], default='O', max_length=1),
        ),
    ]
