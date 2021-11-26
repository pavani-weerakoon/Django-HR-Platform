# Generated by Django 3.2.5 on 2021-11-24 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_candidate_jobs'),
        ('jobs', '0017_auto_20211123_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(default=102, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='users.company'),
        ),
    ]
