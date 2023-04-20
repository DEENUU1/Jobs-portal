from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def send_email_task(email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
