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

admin.site.register(Position)
admin.site.register(Level)
admin.site.register(Country)
admin.site.register(Localization)
admin.site.register(Contract)
admin.site.register(Offer)
admin.site.register(Application)
admin.site.register(Requirements)