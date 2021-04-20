from django.contrib.auth.forms import PasswordChangeForm
from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse


def get_citizen_group():
    citizen_group, created = Group.objects.get_or_create(name='Citizen')
    return citizen_group


def get_organizer_group():
    organizer_group, created2 = Group.objects.get_or_create(name='Organizer')
    print(created2)
    return organizer_group


def home(request):
    return render(request, "meetup/home.html", {"title": "Home"})


def about(request):
    return render(request, "meetup/about.html", {"title": "About"})


def register_initial(request):
    return render(request, "meetup/register_initial.html",
                  {"title": "Register"})


def register_citizen(request):
    if request.method == 'POST':  # If form was filled out and submitted
        form = RegisterCitizenForm(request.POST)
        if form.is_valid():
            form.save()  # Creates User. User's Profile and Wallet created
            # automatically
            name = form.cleaned_data.get('username')
            user = User.objects.filter(username=name).first()
            user.groups.add(get_citizen_group())  # Assigns User to Citizen group

            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, welcome to MeetUp!")
            return redirect("meetup-login")
    else:  # If form not submitted just show form for user to fill out
        form = RegisterCitizenForm()
    return render(request, 'meetup/register.html', {'form': form,
                                                    "title": "Register"})


def register_organizer(request):
    if request.method == 'POST':
        form = RegisterOrganizerForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            user = User.objects.filter(username=name).first()
            user.groups.add(get_organizer_group())

            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, welcome to MeetUp!")
            return redirect("meetup-login")
    else:
        form = RegisterOrganizerForm()
    return render(request, 'meetup/register.html', {'form': form,
                                                    "title": "Register"})


def register_admin(request):
    if request.method == 'POST':
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            user = User.objects.filter(username=name).first()
            user.is_staff = True
            user.is_superuser = True
            user.groups.add(get_citizen_group())
            user.groups.add(get_organizer_group())
            user.save()  # For saving staff and superuser status
            return redirect("admin:index")
    else:
        form = RegisterAdminForm()
    return render(request, 'meetup/register.html', {'form': form,
                                                    "title": "Register Admin"})


def login_user(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('meetup-home')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request,
                                 f"You are now logged in. Welcome, "
                                 f"{username}!")
                return redirect('meetup-home')
            else:
                messages.warning(request, 'Username OR password is incorrect')

        context = {'form': form, 'title': "Login"}
        return render(request, "meetup/login.html", context)


def logout_user(request):
    logout(request)
    return redirect('meetup-login')


@login_required(login_url='meetup-login')
def profile(request):
    context = {'title': f"{request.user}'s Profile",
               'robucks': Wallet.objects.get(user=request.user).balance,
               'credit_cards': CreditCard.objects.filter(user=request.user),
               'events_registered': Event.objects.filter(attendees=request.user),
               'events': Event.objects.filter(user=request.user)}
    return render(request, "meetup/profile.html", context)


@login_required(login_url='meetup-login')
def profile_update(request):
    if request.method == "POST":
        if request.user.groups.filter(name='Citizen').exists() and \
                request.user.groups.filter(name='Organizer').exists():
            u_form = UpdateAdminForm(request.POST, instance=request.user)
        elif request.user.groups.filter(name='Citizen').exists():
            u_form = UpdateCitizenForm(request.POST, instance=request.user)
        else:
            u_form = UpdateOrganizerForm(request.POST, instance=request.user)

        p_form = UpdateProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("meetup-profile")
    else:
        if request.user.groups.filter(name='Citizen').exists() and \
                request.user.groups.filter(name='Organizer').exists():
            u_form = UpdateAdminForm(instance=request.user)
        elif request.user.groups.filter(name='Citizen').exists():
            u_form = UpdateCitizenForm(instance=request.user)
        else:
            u_form = UpdateOrganizerForm(instance=request.user)

        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {'title': f"{request.user.username}'s Profile",
               "u_form": u_form,
               "p_form": p_form
               }
    return render(request, "meetup/profile_update.html", context)


@login_required(login_url='meetup-login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your password was successfully changed!')
            return redirect('meetup-login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    context = {'title': f"Change Password", "form": form}
    return render(request, 'meetup/password_change.html', context)


@login_required(login_url='meetup-login')
def creditcard(request):
    form = CreditCardForm()

    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "Credit card added!")
            return redirect('meetup-profile')

    context = {'form': form, 'title': "Add Credit Card"}
    return render(request, "meetup/creditcard.html", context)


@login_required(login_url='meetup-login')
def wallet(request):
    user_wallet = Wallet.objects.get(user=request.user)
    context = {'robucks': user_wallet.balance}
    return render(request, "meetup/wallet.html", context)


@login_required(login_url='meetup-login')
def payment(request):
    form = PaymentForm(user=request.user, initial={'amount': 0})

    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            user_wallet = Wallet.objects.get(user=request.user)
            amount = form.cleaned_data.get('amount')
            user_wallet.balance += amount
            user_wallet.save(update_fields=['balance'])
            messages.success(request, f"{amount} Robucks added to wallet!")
            return redirect('meetup-wallet')

    context = {'form': form, "title": "Pay"}
    return render(request, "meetup/payment.html", context)


def event_explore(request):
    form = RegisterEventForm()
    
    if request.method == 'POST':
        form = RegisterEventForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                messages.error(request, 'Please log in')
            else:
                event = form.cleaned_data.get('name').first()
                people = event.attendees.all()
                current = User.objects.filter(username=request.user).first()
                event.attendees.set(people)
                event.attendees.add(current)
                messages.success(request, "Registered for event!")
            return redirect("meetup-event-explore")
    
    context = {'form': form, "title": "Explore Events"}
    return render(request, "meetup/event_explore.html", context)
   

def send_coords(request):
    # data = request.POST
    # coords = request.POST.get('coords')
    # data = json.loads(request.POST.get('coords'))
    # data = {
      #  'sent': coords
    # }
    data = ''
    if request.method == 'GET':
        data = list(Event.objects.all().values_list('location'))
        # qs = Event.objects.all().values_list('location')
        # qs_json = serializers.serialize('json', qs)
    return JsonResponse(data, safe=False)
    # return HttpResponse(qs_json, content_type="application/json")
    

class EventDetailView(DetailView):
    model = Event


class EventCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'location','date', 'price', 'max_age', 'min_age', 'capacity',
              'activity_type', 'description', 'contact_info']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    success_url = '/profile/'
    success_message = '%(name)s successfully created!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class EventUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                      UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['name', 'location','date', 'price', 'max_age', 'min_age', 'capacity',
              'activity_type', 'description', 'contact_info']
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.user:
            return True
        return False
    
    success_url = '/profile/'
    success_message = '%(name)s successfully updated!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class EventDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                      UserPassesTestMixin, DeleteView):
    model = Event

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.user:
            return True
        return False
    
    success_url = '/profile/'
    success_message = '%(name)s successfully deleted!'

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        messages.success(self.request, self.success_message % event.__dict__)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)
