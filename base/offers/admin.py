from django.contrib import admin

from .models import (
    CompanyReview
)


@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = [
        'company',
        'email',
        'choose_rate',
        'date_created'
    ]

    list_filter = [
        'company',
        'choose_rate',
        'date_created'
    ]