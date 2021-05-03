from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


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


class UpdateCitizenForm(ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UpdateOrganizerForm(ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='Organization Name')

    class Meta:
        model = User
        fields = ['email', 'first_name']


class UpdateAdminForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class UpdateProfileForm(ModelForm):
    pic = forms.ImageField(label="Profile Picture")

    class Meta:
        model = Profile
        fields = ['pic']


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


class RegisterEventForm(ModelForm):
    name = forms.ModelMultipleChoiceField(label='Select An Event',
                                          queryset=Event.objects.all())

    class Meta:
        model = Event
        fields = ['name']
