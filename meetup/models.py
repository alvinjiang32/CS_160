from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User, Group


# citizen_group, create = Group.objects.get_or_create(name="Citizen")
# organizer_group, create2 = Group.objects.get_or_create(name="Organizer")


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_card_number = models.PositiveIntegerField(validators=[
        MinValueValidator(1000000000000000),
        MaxValueValidator(9999999999999999)])
    expiry_date = models.DateField()
    name = models.CharField(max_length=50)
    cvc_code = models.PositiveIntegerField(validators=[MinValueValidator(100),
                                                       MaxValueValidator(999)])

    def __str__(self):
        return f"{self.name}'s Credit Card"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s Wallet"


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date = models.DateField()
    price = models.PositiveIntegerField(default=0)
    max_age = models.PositiveIntegerField(default=100)
    min_age = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=1)
    activity_type = models.CharField(max_length=25)
    description = models.TextField()
    contact_info = models.TextField()
    attendees = models.JSONField()
