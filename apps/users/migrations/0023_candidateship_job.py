# Generated by Django 3.2.5 on 2021-11-22 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20211122_1114'),
        ('users', '0022_remove_candidateship_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateship',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidateship', to='jobs.job'),
        ),
    ]
