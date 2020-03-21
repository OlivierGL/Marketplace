from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def signup(request):
    return HttpResponse('<h1>Sign-up page</h1>')
