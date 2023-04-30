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


