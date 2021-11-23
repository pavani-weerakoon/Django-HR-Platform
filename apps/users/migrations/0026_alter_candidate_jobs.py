# Generated by Django 3.2.5 on 2021-11-22 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_remove_interview_candidateship'),
        ('users', '0025_auto_20211122_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='jobs',
            field=models.ManyToManyField(
                related_name='candidates', through='jobs.Candidateship', to='jobs.Job', blank=True),
        ),

    ]
