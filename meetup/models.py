from django.db import models
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# each class = table, each attribute = field in table

class CreditCard(models.Model):
    name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=200)
    Expiration = models.CharField(max_length=200)
    cvc = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' ' + self.creditcardnumber + ' ' + self.creditcardexpire + ' ' + self.cvc


