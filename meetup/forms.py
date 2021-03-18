from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CreditCard, Event


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    groups = forms.CharField(label='Type of Account', widget=forms.Select(
        choices=[('Citizen', 'Citizen'), ('Organizer', 'Organizer')]))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'groups']


class LoginForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class CreditCardForm(ModelForm):
    expiry_date = forms.DateField(label='Expiry Date',
                                  widget=forms.TextInput(attrs={'placeholder':
                                                                'MM/DD/YYYY'}))

    class Meta:
        model = CreditCard
        
        fields = ['name', 'credit_card_number', 'expiry_date',
                  'cvc_code']

class EventForm(ModelForm):

    class Meta:
        model = Event
        
        fields = ['user', 'name', 'location', 'date', 'price', 
                 'max_age', 'min_age', 'capacity', 'activity_type',
                 'description', 'contact_info', 'attendees']
    