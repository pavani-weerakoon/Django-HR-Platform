# Generated by Django 3.2.5 on 2021-11-22 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_remove_interview_candidateship'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='candidateship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='jobs.candidateship'),
        ),
    ]
