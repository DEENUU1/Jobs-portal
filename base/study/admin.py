from django.contrib import admin

from .models import Category, Resources


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]

    list_filter = ["name"]


@admin.register(Resources)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "url", "date_created"]

    list_filter = ["name", "category", "date_created"]
