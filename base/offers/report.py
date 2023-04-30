from django.db.models import Avg
from offers.models import CompanyReview


def calculate_avg_rating(company):
    avg_rating = CompanyReview.objects.filter(company=company).aggregate(Avg('choose_rate'))
    return avg_rating['choose_rate__avg']