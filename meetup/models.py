from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    pic = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    def __str(self):
        return self.name


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_card_number = models.PositiveBigIntegerField(validators=[
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
    balance = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(1000)])

    def __str__(self):
        return f"{self.user}'s Wallet"


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          unique=True)
    user = models.ForeignKey(User, related_name='event_owner',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.JSONField()
    date = models.DateField()
    price = models.PositiveIntegerField(default=0)
    max_age = models.PositiveIntegerField(default=100)
    min_age = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=1)
    activity_type = models.CharField(max_length=25)
    description = models.TextField()
    contact_info = models.TextField()
    attendees = models.ManyToManyField(User, related_name='event_attendees',
                                       blank=True)

    def __str__(self):
        return f"{self.user}'s Event: {self.name}"

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.id})
