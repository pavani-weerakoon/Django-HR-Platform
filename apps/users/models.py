from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import uuid

from safedelete.models import SafeDeleteModel

from apps.common.email_templates import EmailTemplates
from apps.common.services import generate_token, send_mail


class UserType(models.TextChoices):
    CANDIDATE = 'CANDIDATE', _('CANDIDATE')
    INTERVIEWER = 'INTERVIEWER', _('INTERVIEWER')
    ADMIN = 'ADMIN', _('ADMIN')


class Company(SafeDeleteModel):
    name = models.BinaryField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True,
                              related_name='managing_company')
    created_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    company_email = models.EmailField(max_length=200, blank=True, null=True)


class User(AbstractUser, SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
        default=UserType.ADMIN,
    )
    company = models.ForeignKey(
        Company, related_name='company_user',
        null=True,
        on_delete=models.CASCADE,
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_admin(self):
        return self.user_type == UserType.ADMIN

    def is_candidate(self):
        return self.user_type == UserType.CANDIDATE

    def is_interviewer(self):
        return self.user_type == UserType.INTERVIEWER

    def generate_email_verification_code(self):
        verification = self.email_verifications.create(code=generate_token(6))
        send_mail(
            'Please confirm your email.',
            self.email,
            EmailTemplates.AUTH_VERIFICATION,
            {'verification_code': verification.code}
        )


class UserEmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='email_verifications'
    )
    code = models.PositiveIntegerField(max_length=6)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Admin(models.Model):
    admin_role = models.CharField(
        max_length=200,
    )
    user = models.OneToOneField(
        User, related_name='company_admin',
        on_delete=models.CASCADE,
        max_length=200,

    )


class Candidate(models.Model):

    jobs = models.ManyToManyField(
        'jobs.Job', related_name='candidates', through='jobs.Candidateship',
    )
    user = models.OneToOneField(
        User, related_name='candidate',
        on_delete=models.CASCADE,
        max_length=200,

    )


class Interviewer(models.Model):
    role = models.CharField(
        max_length=200,
    )
    user = models.OneToOneField(
        User, related_name='Interviewers',
        on_delete=models.CASCADE,
        max_length=200,

    )
