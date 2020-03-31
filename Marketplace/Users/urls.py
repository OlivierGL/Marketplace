from django.urls import path, include
from . import views

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('login/', views.do_login, name='login'),
  path('logout/', views.do_logout, name='logout'),
  path('profile/', views.profile, name='profile'),
]
