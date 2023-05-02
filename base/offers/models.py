from accounts.models import CustomUser
from django.db import models


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
    username = models.CharField(max_length=30, default="Anonimous")
    date_created = models.DateTimeField(auto_now_add=True)
    short_description = models.CharField(max_length=200)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def return_formatted_rate(self):
        """
        A property that returns the rating of the review in a formatted way.
        """
        return f"{self.choose_rate}/5"

    class Meta:
        ordering = ('date_created',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.choose_rate
