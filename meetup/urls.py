from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='meetup-home'),
    path('about/', views.about, name='meetup-about'),
    path('register/', views.register, name='meetup-register'),
    path('login/', views.login_user, name="meetup-login"),
    path('creditcard/', views.creditcard, name='meetup-creditcard'),
    path('logout/', views.logout_user, name='meetup-logout'),
    path('register_initial/', views.register_initial, name='meetup-register_initial'),
    path('event_form/', views.event_form, name="meetup-event_form")
]