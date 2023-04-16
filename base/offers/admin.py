from django.contrib import admin
from .models import (
    Position,
    Level,
    Country,
    Localization,
    Contract,
    Offer
)

admin.site.register(Position)
admin.site.register(Level)
admin.site.register(Country)
admin.site.register(Localization)
admin.site.register(Contract)
admin.site.register(Offer)