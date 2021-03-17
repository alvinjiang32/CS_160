from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='meetup-home'),
    path('about/', views.about, name='meetup-about'),
    path('register/', views.register, name='meetup-register'),
]