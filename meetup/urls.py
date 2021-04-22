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
    path('contact/', views.contact, name="meetup-contact"),
    path('login/', views.login_user, name="meetup-login"),
    path('logout/', views.logout_user, name='meetup-logout'),
    path('profile/', views.profile, name='meetup-profile'),
    path('profile-update/', views.profile_update,
         name="meetup-profile-update"),
    path('password-change', views.password_change,
         name='meetup-password-change'),
    path('event-explore/', views.event_explore, name="meetup-event-explore"),
    path('send-coords/', views.send_coords, name="meetup-send-coords"),
    path('events/new/', views.EventCreateView.as_view(), name="event-create"),
    path('events/<uuid:pk>/', views.EventDetailView.as_view(), name="event-detail"),
    path('events/<uuid:pk>/update', views.EventUpdateView.as_view(), name="event-update"),
    path('events/<uuid:pk>/delete', views.EventDeleteView.as_view(), name="event-delete"),
    
    path('creditcard/', views.creditcard, name='meetup-creditcard'),
    path('wallet/', views.wallet, name='meetup-wallet'),
    path('payment/', views.payment, name='meetup-payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
