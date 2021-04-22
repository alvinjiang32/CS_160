from django.contrib import admin
from .models import CreditCard, Wallet, Event, Profile, Contact

admin.site.register(Profile)
admin.site.register(CreditCard)
admin.site.register(Wallet)
admin.site.register(Contact)
admin.site.register(Event)
