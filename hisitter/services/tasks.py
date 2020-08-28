""" Users celery tasks."""
# Python
import datetime

# Django imports
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Celery imports
from celery.decorators import task

# Models
from hisitter.users.models import User


@task(name='create_a_service_mail', max_retries=3)
def create_a_service_email(
    client_username,
    bbs_username,
    client_email,
    bbs_email,
    date,
    shift):
    """Send a schedule confirmation."""
    subject = f'Hi @{client_username}! you are schedule a Babysitter'
    from_email = 'Hisitter <noreply@hisitter.xyz'
    content = render_to_string(
        'emails/services/create_confirmation_email.html',
        {'client':client_username, 'Babysitter': bbs_username, 'date': date, 'shift': shift}
    )
    msg = EmailMultiAlternatives(
        subject,
        content,
        from_email,
        [bbs_email, client_email])
    msg.attach_alternative(content, "text/html")
    msg.send()
