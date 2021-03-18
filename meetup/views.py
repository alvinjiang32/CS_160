from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "meetup/home.html", {"title": "Home"})


def about(request):
    return render(request, "meetup/about.html", {"title": "About"})


citizen_group, created = Group.objects.get_or_create(name='Citizen')
organizer_group, created2 = Group.objects.get_or_create(name='Organizer')

def register_initial(request):
    return render(request, "meetup/register_initial.html", {"title": "Register Initial"})

def register(request):
    if request.method == 'POST':  # If form was filled out and submitted
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Creates User

            name = form.cleaned_data.get('username')
            group = form.cleaned_data.get('groups')
            user = User.objects.filter(username=name).first()
            if group == "Citizen":  # Assigns group to User's groups field
                user.groups.add(citizen_group)
            else:
                user.groups.add(organizer_group)

            wallet = Wallet(user=user)  # Creates Wallet for User
            wallet.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, welcome to MeetUp!")
            return redirect("meetup-login")
    else:  # If form not submitted just show form for user to fill out
        form = UserRegisterForm()
    return render(request, 'meetup/register.html', {'form': form})


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

        context = {'form': form}
        return render(request, "meetup/login.html", context)


def logout_user(request):
    logout(request)
    return redirect('meetup-home')


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
            return redirect('meetup-creditcard')

    context = {'form': form}
    return render(request, "meetup/creditcard.html", context)


def event_form(request):
    return render(request, "meetup/event_form.html", { "title": "Event_Form"})
