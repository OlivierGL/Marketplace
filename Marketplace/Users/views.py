from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserInfo, Address
from . import forms
from django.db import IntegrityError
from Market import models as market_models
from Chat import models as chat_models
from django.db.models import Q


# Create your views here.


def signup(request):
    context = {'activeNavItem': 'signup',
               'areaConstraintMessage': 'Our service is currently only available in the Montreal area.'}

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                user_db = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'])

                user_info_db = UserInfo.objects.create(
                    user=user_db,
                    rating=0,
                    phone_number=form.cleaned_data['phone_number']
                )

                Address.objects.create(
                    country=form.cleaned_data['country'],
                    province=form.cleaned_data['province'],
                    city=form.cleaned_data['city'],
                    street_address=form.cleaned_data['street_address'],
                    postal_code=form.cleaned_data['postal_code'],
                    user=user_info_db
                )

                market_models.Cart.objects.create(user=user_info_db)

                return authenticate_and_login(request, form, context)
            except IntegrityError:
                form.add_error('username', 'Username is taken')
    else:
        form = forms.SignupForm(initial={'country': 'Canada',
                                         'province': 'Quebec',
                                         'city': 'Montreal'})

    context['form'] = form
    return render(request, 'Users/signup.html', context)


def do_login(request):
    context = {'activeNavItem': 'login'}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            return authenticate_and_login(request, form, context)
        context['form'] = form
    return render(request, 'Users/login.html', context)


@login_required
def do_logout(request):
    logout(request)
    messages.info(request, 'Logout successful')
    return HttpResponseRedirect(reverse('login'))


def authenticate_and_login(request, form, context):
    user = authenticate(request,
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    if user is not None:
        login(request, user)
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        messages.success(request, 'Login successful')
        return HttpResponseRedirect(reverse('market-home'))
    else:
        messages.error(request, 'Unable to log in')
        context['form'] = form
        return render(request, 'Users/login.html', context)

@login_required
def profile(request, primary_key):
     
    user_data = User.objects.get(pk=primary_key)
    user_info = UserInfo.objects.get(user=user_data)
    address = user_info.user_address.first()
    current_user_info = UserInfo.objects.get(user=request.user)
    chats = chat_models.Room.objects.filter(Q(user1=current_user_info) | Q(user2=current_user_info))

    rooms = []
    for room in chats:
        if current_user_info != room.user1:
            correspondent = room.user1
        else:
            correspondent = room.user2
        rooms.append((room, correspondent))

    # Disabling the navbar bold text for My Profile if we're not visiting the
    # current user's profile.
    if user_info == current_user_info:
        context = {
            'items': market_models.Product.objects.filter(artist=user_info),
            'user_info': user_info,
            'current_user_info': current_user_info,
            'address': address,
            'activeNavItem': "myProfile",
            'noProductErrorMessage': "You have no products for sale.",
            'noProductSubMessage': "Sell products by clicking on the \"Add a new product\" button.",
            'chat_rooms': rooms,
        }
    else:
        context = {
            'items': market_models.Product.objects.filter(artist=user_info),
            'user_info': user_info,
            'current_user_info': current_user_info,
            'address': address,
            'activeNavItem': "",
            'noProductErrorMessage': "This user has no products for sale."
        }

    return render(request, 'Users/profile.html', context)
