from django.shortcuts import render
from django.contrib.auth.models import User
from . import forms
from django.db import IntegrityError


# Create your views here.


def signup(request):
    context = {'activeNavItem': 'signup'}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'])

                return render(request, 'Market/home.html')
            except IntegrityError:
                form.add_error('username', 'Username is taken')
        context['form'] = form

    return render(request, 'Users/signup.html', context)
