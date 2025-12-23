""" Users celery tasks."""

# Django imports
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

# Celery imports
from celery import shared_task

# Models
from hisitter.users.models import User

# Utilities
import jwt
from datetime import timedelta


def gen_verification_token(username):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


@shared_task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(username, email):
    """Send account verification link to given user."""
    verification_token = gen_verification_token(username)
    subject = f'Welcome @{username}! verify your account to start find a babysitter'
    from_email = 'Hisitter <noreply@hisitter.xyz'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'username': username, 'base_url': settings.EMAIL_VERIFICATION_HOST}
    )
    msg = EmailMultiAlternatives(
        subject,
        content,
        from_email,
        [email, 'ricardo.ares1989@gmail.com', 'restrada@ideartec.com.mx', 'nathanabdiel1@gmail.com']
    )
    msg.attach_alternative(content, "text/html")
    msg.send()
