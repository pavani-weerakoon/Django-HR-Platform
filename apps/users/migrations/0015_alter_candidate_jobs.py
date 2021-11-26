# Generated by Django 3.2.5 on 2021-11-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20211122_1114'),
        ('users', '0014_auto_20211122_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='jobs',
        ),
        migrations.AddField(
            model_name='candidate',
            name='jobs',
            field=models.ManyToManyField(
                related_name='candidates',  to='jobs.Job'),
        ),
    ]
