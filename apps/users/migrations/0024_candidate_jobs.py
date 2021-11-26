# Generated by Django 3.2.5 on 2021-11-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20211122_1114'),
        ('users', '0023_candidateship_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='jobs',
            field=models.ManyToManyField(related_name='candidates', through='users.Candidateship', to='jobs.Job'),
        ),
    ]
