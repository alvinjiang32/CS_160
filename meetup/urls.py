from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='meetup-home'),
    path('about/', views.about, name='meetup-about'),
    path('login/', views.login, name="meetup-login"),
    path('register/', views.register,name='meetup-register'),
    path('creditcard/', views.creditcard, name='meetup-creditcard'),
    path('logout/', views.logoutUser, name='meetup-logout'),
]