from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """
    A custom user model that extends the built-in Django AbstractUser model.
    The model includes additional fields for role, first name, last name, phone number, description, and image.
    Attributes:
        role: A CharField containing the role of the user, which can be either "company" or "user".
        first_name: A CharField containing the first name of the user.
        last_name: A CharField containing the last name of the user.
        phone_number: A PhoneNumberField containing the phone number of the user.
        description: A CharField containing a description of the user.
        image: An ImageField containing an image of the user.
    """
    ROLE = (
        ('company', 'company'),
        ('user', 'user')
    )

    role = models.CharField(max_length=10, choices=ROLE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        A method that overrides the built-in save method to ensure that the
        first_name and last_name fields are set to None for users with a role of "company".
        """
        if self.role == "company":
            self.first_name = None
            self.last_name = None

        super().save(*args, **kwargs)


class CompanyReview(models.Model):
    """
    A  model that represents a review of a company.
    Attributes:
        choose_rate: A PositiveIntegerField containing the rating of the review.
        email: A EmailField containing the email of the reviewer.
        date_created: A DateTimeField containing the date the review was created.
        short_description: A CharField containing a short description of the review.
    """
    RATES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    choose_rate = models.PositiveIntegerField(choices=RATES)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    short_description = models.CharField(max_length=200)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
