# Generated by Django 3.2.5 on 2021-11-22 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20211122_1114'),
        ('users', '0013_alter_candidate_jobs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidateship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidateship', to='users.candidate')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidateship', to='jobs.job')),
            ],
        ),
        migrations.AlterField(
            model_name='candidate',
            name='jobs',
            field=models.ManyToManyField(related_name='candidates', through='users.Candidateship', to='jobs.Job'),
        ),
    ]