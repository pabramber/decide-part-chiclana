from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='a_community',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='born_year',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='city',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='civil_state',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='gender',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='name',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='sexuality',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='surname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='census',
            name='works',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='census',
            unique_together={('voting_id', 'voter_id', 'name', 'surname', 'city', 'a_community', 'gender', 'born_year', 'civil_state', 'sexuality', 'works')},
        ),
    ]
