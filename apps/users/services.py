from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from apps.common.email_templates import EmailTemplates
from apps.common.services import send_mail
from apps.users.models import Candidate, User


def request_password_reset(user):
    token = default_token_generator.make_token(user)
    reset_url = '{}/reset-password?email={}&token={}'.format(
        settings.APP_URL, user.email, token)
    data = {"reset_url": reset_url}
    send_mail(
        'Password Reset Confirmation',
        user.email,
        EmailTemplates.AUTH_PASSWORD_RESET_REQUEST,
        data
    )


def create_candidate_user(data, request):
    candidate_user = User.objects.create(
        username=data['email'],
        email=data['email'],
        company=request.user.company,
        user_type="CANDIDATE"
    )
    candidate_user.set_password("home")
    candidate_user.save()
    candidate = Candidate.objects.create(user=candidate_user)
    candidate.save()
    return candidate
