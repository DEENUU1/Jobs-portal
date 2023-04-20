from celery import shared_task
from django.core.mail import send_mail
import time 


@shared_task(serializer='json', name='send_mail')
def send_email_func(subject, message, from_email, receiver):
    time.sleep(20)
    send_mail(subject, message, from_email, receiver)
    return 'Mail Sent Successfully'