from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import forms, ModelForm
from .models import CreditCard
from django.contrib.auth.forms import UserCreationForm


class PaymentForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LogUserInForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
