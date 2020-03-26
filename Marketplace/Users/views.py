from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserInfo, Address
from . import forms
from django.db import IntegrityError


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

                address_db = Address.objects.create(
                    country=form.cleaned_data['country'],
                    province=form.cleaned_data['province'],
                    city=form.cleaned_data['city'],
                    street_address=form.cleaned_data['street_address'],
                    postal_code=form.cleaned_data['postal_code'],
                )

                UserInfo.objects.create(
                    user=user_db,
                    address=address_db,
                    rating=0
                )

                return authenticate_and_login(request, form)
            except IntegrityError:
                form.add_error('username', 'Username is taken')
    else:
        form = forms.SignupForm()

    context['form'] = form
    return render(request, 'Users/signup.html', context)


def do_login(request):
    context = {'activeNavItem': 'login'}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            return authenticate_and_login(request, form)
        context['form'] = form
    return render(request, 'Users/login.html', context)


def authenticate_and_login(request, form):
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
