
# Jobs portal
### Django web application with IT Jobs Offers
 

This project allows companies to add job offers and manage applications from candidates.The company can also generate reports in the form of a .csv file for each offer. 

On the other hand, users can filter, search, and apply for jobs, as well as rate companies and write reviews.

Thanks to the use of Celery and Redis technologies, the application can send an asynchronous e-mail with confirmation when registering an account.

```python
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
```

## Technologies:
- Python 
- Django 
- Celery 
- Redis 
- Docker
- HTML & Bootstrap

## Ideas for development
- Google / Github registration 
- More details and information about company (team, tech stack, integration with social media and more)


## Tests 
To run unit tests you need to this command
```bash
python manage.py test <APPLICATION_NAME>.tests
```
You can run tests for applications:
- offers
- dashboard
- accounts
- study
## Installation


1. First you need to clone this repository
```bash
git clone <link>
```
2. Andd .env file in base directory (there where settings.py)
```bash
SECURITY_CODE=<DJANGO-SECURITY-CODE-HERE>
GMAIL_PASSWORD=<YOUR-GMAIL-PASSWORD-HERE>
GMAIL_EMAIL=<YOUR-GMAIL-EMAIL-HERE>
```
3. Go to main directory
```bash
cd base
```
4. Then install all requirements 
```bash
pip install -r requirements.txt
```
5. Make migrations 
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Create superuser
```bash
python manage.py createsuperuser
```

### If you wanna use docker just use this command
```bash
docker-compose up
```



## Authors

- [@DEENUU1](https://www.github.com/DEENUU1)

