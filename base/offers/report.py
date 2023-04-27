from django.db.models import Avg
from accounts.models import CompanyReview


def calculate_avg_rating(company):
    avg_rating = CompanyReview.objects.filter(company=company).aggregate(Avg('choose_rate'))
    return round(avg_rating['choose_rate__avg'], 1)