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
    return render(request, "meetup/register_initial.html",
                  {"title": "Register"})


def register_citizen(request):
    if request.method == 'POST':  # If form was filled out and submitted
        form = RegisterCitizenForm(request.POST)
        if form.is_valid():
            form.save()  # Creates User
            name = form.cleaned_data.get('username')
            user = User.objects.filter(username=name).first()
            user.groups.add(citizen_group)  # Assigns User to Citizen group
            user_wallet = Wallet(user=user)  # Creates Wallet for User
            user_wallet.save()

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
            form.save()  # Creates User
            name = form.cleaned_data.get('username')
            user = User.objects.filter(username=name).first()
            user.groups.add(organizer_group)
            user_wallet = Wallet(user=user)
            user_wallet.save()

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
            user.groups.add(citizen_group)
            user.groups.add(organizer_group)
            user.save()  # For saving staff and superuser status
            user_wallet = Wallet(user=user)
            user_wallet.save()
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

    context = {'form': form, 'title': "Add Credit Card"}
    return render(request, "meetup/creditcard.html", context)

  
# @login_required(login_url='meetup-login')
def event_form(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()  # Save form

            name = form.cleaned_data.get('name')

            user = User.objects.filter(username=name).first()

            username = form.cleaned_data.get('name')
            messages.success(request, f"Event: {name} Successfully Created!")
            return redirect("meetup-event_form")
        
    context = {'form': form}

    return render(request, "meetup/event_form.html", context)


@login_required(login_url='meetup-login')
def wallet(request):
    user_wallet = Wallet.objects.get(user=request.user)
    context = {'username': request.user.username,
               'robucks': user_wallet.balance}
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

