from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import uuid

from safedelete.models import SafeDeleteModel

from apps.common.email_templates import EmailTemplates
from apps.common.services import generate_token, send_mail
from apps.jobs.models import Job


class UserType(models.TextChoices):
    CANDIDATE = 'CANDIDATE', _('CANDIDATE')
    INTERVIEWER = 'INTERVIEWER', _('INTERVIEWER')
    ADMIN = 'ADMIN', _('ADMIN')


class Company(SafeDeleteModel):
    name = models.BinaryField(max_length=100, null=True, blank=True)
    owner = models.OneToOneField('users.User', on_delete=models.CASCADE,
                                 related_name='managing_company', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200,)
    company_email = models.EmailField(max_length=200, blank=True, null=True)


class User(AbstractUser, SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
    )
    company = models.ForeignKey(
        Company, related_name='company_user',
        on_delete=models.CASCADE,
    )

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


class Interviewer(models.Model):
    role = models.CharField(
        max_length=200,
    )
    user = models.OneToOneField(
        User, related_name='Interviewers',
        on_delete=models.CASCADE,
        max_length=200,

    )


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
    cv = models.FilePathField(
        null=True, blank=True
    )
    jobs = models.ManyToManyField(
        Job, related_name='candidates'

    )
    user = models.OneToOneField(
        User, related_name='candidates',
        on_delete=models.CASCADE,
        max_length=200,

    )
