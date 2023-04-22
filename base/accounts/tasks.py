from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
import csv
from offers.models import Application, Offer



@shared_task()
def send_email_task(email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)


@shared_task()
def generate_csv_file(pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full name', 'Email', 'Expected pay', 'Linkedin', 'Portfolio'])

    application = Application.objects.filter(offer__id=pk)

    for data in application:
        writer.writerow([data.return_full_name, data.email, data.expected_pay, data.linkedin, data.portfolio])

    return response