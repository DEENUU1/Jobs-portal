from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "role",
        "is_active",
        "username",
        "email",
        "first_name",
        "last_name",
        "username",
    ]

    list_filter = ["role", "is_active"]
