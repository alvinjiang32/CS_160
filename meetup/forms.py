from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    groups = forms.CharField(label='Type of Account', widget=forms.Select(
        choices=[('Citizen', 'Regular'), ('Organizer', 'Organizer')]))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'groups']

