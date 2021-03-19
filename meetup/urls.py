from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='meetup-home'),
    path('about/', views.about, name='meetup-about'),
    path('register-initial/', views.register_initial,
         name='meetup-register-initial'),
    path('register-citizen/', views.register_citizen,
         name='meetup-register-citizen'),
    path('register-organizer/', views.register_organizer,
         name='meetup-register-organizer'),
    path('register-admin/', views.register_admin,
         name='meetup-register-admin'),
    path('login/', views.login_user, name="meetup-login"),
    path('logout/', views.logout_user, name='meetup-logout'),
    path('creditcard/', views.creditcard, name='meetup-creditcard'),
    path('wallet/', views.wallet, name='meetup-wallet'),
    path('payment/', views.payment, name='meetup-payment'),
]
