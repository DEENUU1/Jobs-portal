from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email_task(email, subject, message):
    """
    A Celery task that sends an email to a specified email address with a given subject and message.
    Parameters:
        email: A string containing the email address to send the email to.
        subject: A string containing the subject of the email.
        message: A string containing the message to be included in the email.
    """
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
