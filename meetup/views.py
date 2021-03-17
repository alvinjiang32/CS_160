from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import PaymentForm, CreateUserForm, LogUserInForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "meetup/home.html", {"title": "Home"})


def about(request):
    return render(request, "meetup/about.html", {"title": "About"})


def login(request):
    form = LogUserInForm()
    if request.user.is_authenticated:
        return redirect('meetup-home')
    else:
        if request.method == 'POST':
            form = LogUserInForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username =username, password=password)
            if user is not None:
                login(request, username)
                return redirect('meetup-home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {'form': form}
        return render(request, "meetup/login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('meetup-login')

#@login_required(login_url='meetup-login')
def creditcard(request):

    formx = PaymentForm()

    if request.method == 'POST':
        formx = PaymentForm(request.POST)
        if formx.is_valid():
            formx.save()



    context = {'form':formx}
    return render(request, "meetup/creditcard.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect('meetup-home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success((request, 'Account was created for' + user))
                return redirect('meetup-login')

        context = {'form': form}
        return render(request, 'meetup/register.html', context)


