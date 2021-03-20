from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from django.forms import ModelForm
from .models import CreditCard, Event


class RegisterCitizenForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1',
                  'password2']


class RegisterOrganizerForm(UserCreationForm):
    email = forms.EmailField(label='Organization Email')
    first_name = forms.CharField(label='Organization Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']


class RegisterAdminForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2']


class LoginForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class CreditCardForm(ModelForm):
    expiry_date = forms.DateField(label='Expiry Date',
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'MM/DD/YYYY'}))
    credit_card_number = forms.IntegerField(label='Credit Card Number')
    cvc_code = forms.IntegerField(label='CVC Code')

    class Meta:
        model = CreditCard
        
        fields = ['name', 'credit_card_number', 'expiry_date',
                  'cvc_code']


class EventForm(ModelForm):
    date = forms.DateField(label='Date',
                                  widget=forms.TextInput(attrs={'placeholder':
                                                                'MM/DD/YYYY'}))
    name = forms.CharField(label='Event Name')
    attendees = forms.CharField()

    class Meta:
        model = Event
        
        fields = ['user', 'name', 'location', 'date', 'price', 
                 'max_age', 'min_age', 'capacity', 'activity_type',
                 'description', 'contact_info', 'attendees']

        
class PaymentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields['amount'] = forms.IntegerField(
            validators=[MinValueValidator(0)],
            label='Amount'
        )
        self.fields['credit_card'] = forms.ModelChoiceField(
            queryset=CreditCard.objects.filter(user=self.user),
            empty_label="-------",
            label="Credit Card"
        )
