""" Users celery tasks."""

# Django imports
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

# Celery imports
from celery.decorators import task, periodic_task
from config import celery_app

# Models
from hisitter.users.models import (
                            User
                        )

# Utilities
import jwt
from datetime import timedelta

def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = f'Welcome @{user.username}! verify your account to start find a babysitter'
    from_email = 'Hisitter <noreply@hisitter.xyz'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token':verification_token, 'user':user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
