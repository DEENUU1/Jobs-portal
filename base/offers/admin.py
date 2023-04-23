from django.contrib import admin

from .models import (
    Position,
    Level,
    Country,
    Localization,
    Contract,
    Offer,
    Application,
    Requirements
)


@admin.register(Position)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'position_name'
    ]

    list_filter = [
        'position_name'
    ]


@admin.register(Level)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'level_name'
    ]

    list_filter = [
        'level_name'
    ]


@admin.register(Country)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

    list_filter = [
        'name'
    ]


@admin.register(Localization)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'city',
        'country'
    ]

    list_filter = [
        'country',
        'city'
    ]


@admin.register(Contract)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'contract_type'
    ]

    list_filter = [
        'contract_type'
    ]


@admin.register(Requirements)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

    list_filter = [
        'name'
    ]


class ApplicationInline(admin.TabularInline):
    model = Application


@admin.register(Offer)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'company',
        'position',
        'level',
        'remote',
        'date_created'
    ]

    list_filter = [
        'position',
        'level',
        'contract',
        'requirements',
        'salary_from',
        'salary_to',
        'remote'
    ]

    list_editable = [
        'company',
        'position',
        'level'
    ]

    inlines = [ApplicationInline]


@admin.register(Application)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'offer',
        'answer',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'date_created',
        'portfolio',
        'linkedin',
        'cv'
    ]

    list_filter = [
        'offer',
        'date_created',
        'answer'
    ]
