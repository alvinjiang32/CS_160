from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Wallet


def home(request):
    return render(request, "meetup/home.html", {"title": "Home"})


def about(request):
    return render(request, "meetup/about.html", {"title": "About"})


citizen_group, created = Group.objects.get_or_create(name='Citizen')
organizer_group, created2 = Group.objects.get_or_create(name='Organizer')


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
            return redirect("meetup-home")  # REDIRECT TO LOGIN
    else:  # If form not submitted just show form for user to fill out
        form = UserRegisterForm()
    return render(request, 'meetup/register.html', {'form': form})
