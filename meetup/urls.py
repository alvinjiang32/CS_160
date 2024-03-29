from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


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
    path('contact/', views.contact, name="meetup-contact"),
    path('profile/', views.profile, name='meetup-profile'),
    path('profile/update/', views.profile_update,
         name="meetup-profile-update"),
    path('password-change/', views.password_change,
         name='meetup-password-change'),
    path('events/', views.events, name="meetup-events"),
    path('event/create', views.EventCreateView.as_view(),
         name="event-create"),
    path('event/<uuid:pk>/', views.EventDetailView.as_view(),
         name="event-detail"),
    path('event/<uuid:pk>/update', views.EventUpdateView.as_view(),
         name="event-update"),
    path('event/<uuid:pk>/delete', views.EventDeleteView.as_view(),
         name="event-delete"),
    path('send-coords/', views.send_coords, name="meetup-send-coords"),
    path('credit-card/', views.credit_card, name='meetup-credit-card'),
    path('wallet/', views.wallet, name='meetup-wallet'),
    path('payment/', views.payment, name='meetup-payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
