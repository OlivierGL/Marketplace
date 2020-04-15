from django.urls import path
from . import views

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('login/', views.do_login, name='login'),
  path('logout/', views.do_logout, name='logout'),
  path('profile/<int:primary_key>/', views.profile, name='profile'),
]
