# Generated by Django 3.2.5 on 2021-11-16 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_experience_interview_question_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='role',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='time_period',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='worked_place',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]