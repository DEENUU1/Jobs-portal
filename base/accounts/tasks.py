from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage


@shared_task()
def send_email_task(email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)


@shared_task()
def activation_email_task(email, message):
    send_mail(EmailMessage(
        subject="Activate your account",
        message=message,
        to=[email],
    ))