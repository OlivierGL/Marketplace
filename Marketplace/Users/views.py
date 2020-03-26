from django.shortcuts import render
from django.contrib.auth.models import User
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

                return render(request, 'Market/home.html')
            except IntegrityError:
                form.add_error('username', 'Username is taken')
        context['form'] = form
    else:
        form = forms.SignupForm()

    context['form'] = form
    return render(request, 'Users/signup.html', context)
