# Generated by Django 3.2.5 on 2021-11-25 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_candidate_jobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='cv',
        ),
    ]