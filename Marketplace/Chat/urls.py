from django.urls import path
from . import views


urlpatterns = [
	path('<int:user_info_pk>/<int:current_user_info_pk>/', views.find_room, name='find_room'),
    path('<int:room_pk>/', views.room, name='room'),
    path('<int:room_pk>/delete/', views.roomDelete, name="delete-room")
]