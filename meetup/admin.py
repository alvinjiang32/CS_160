from django.contrib import admin
from .models import CreditCard, Wallet, Event

admin.site.register(CreditCard)
admin.site.register(Wallet)
admin.site.register(Event)