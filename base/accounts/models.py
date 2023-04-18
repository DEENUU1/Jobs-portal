from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):

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
        if self.role == "company":
            self.first_name = None
            self.last_name = None

        super().save(*args, **kwargs)
