from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from apps.users.models import User, Company, Interviewer, Admin, Candidate

# Create your models here.


class Job(models.Model):
    role = models.CharField(
        max_length=200,
    )
    salary = models.IntegerField(
        null=True
    )
    company = models.ForeignKey(
        Company,  related_name='jobs',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.role


class Section(models.Model):
    section_name = models.CharField(
        max_length=200,
    )

    def __str__(self):
        return self.section_name


class Question(models.Model):
    question_type = models.CharField(
        max_length=200,
    )
    section = models.ForeignKey(
        Section,  related_name='questions',
        on_delete=models.CASCADE,
    )
    job = models.ForeignKey(
        Job, related_name='questions',
        on_delete=models.CASCADE,
    )

    # def __str__(self):
    #     return self.question_type


class Interview(models.Model):
    interviewer = models.ForeignKey(
        Interviewer, related_name='interviews',
        on_delete=models.CASCADE,
    )
    candidate = models.ForeignKey(
        Candidate, related_name='interviews',
        on_delete=models.CASCADE,
    )


class Experience(models.Model):
    role = models.CharField(
        max_length=200,
    )
    worked_place = models.CharField(
        max_length=100,
    )
    time_period = models.CharField(
        max_length=200,
    )
    Candidate = models.ForeignKey(
        Candidate, related_name='experiences',
        on_delete=models.CASCADE,
    )
