from django.contrib import admin

from .models import CustomUser, CompanyReview


@admin.register(CustomUser)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'role',
        'is_active',
        'username',
        'email',
        'first_name',
        'last_name',
        'username'
    ]

    list_filter = [
        'role',
        'is_active'
    ]

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