from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Users import models as user_models
from . import models


# View that generates the Chat page.
@login_required
def room(request, room_pk=None):
	room = models.Room.objects.get(pk=room_pk)
	# Getting the messages that were sent previously in the room
	chat_messages = models.Message.objects.filter(room=room)
	user_info = user_models.UserInfo.objects.get(user=request.user)
	# Making sure only the chat users can join.
	if user_info != room.user1 and user_info != room.user2:
		raise PermissionDenied()

	context = {
		'room': room,
		'chat_messages': chat_messages,
		'user': request.user
	}
	return render(request, 'Chat/room.html', context)


# This function is used to find the appropriate room for the user based on its pk and the contacted user's pk
# it redirects to the proper url with the proper room pk
@login_required
def find_room(request, user_info_pk, current_user_info_pk):
	# The user1 field in a chat object is the user with the smaller pk
	if user_info_pk < current_user_info_pk:
		user1Obj = user_models.UserInfo.objects.get(pk=user_info_pk)
		user2Obj = user_models.UserInfo.objects.get(pk=current_user_info_pk)
	else:
		user2Obj = user_models.UserInfo.objects.get(pk=user_info_pk)
		user1Obj = user_models.UserInfo.objects.get(pk=current_user_info_pk)

	# Getting the room reserved for the two users
	roomQuerry = models.Room.objects.filter(user1=user1Obj, user2=user2Obj)
	if roomQuerry.exists():
		room = roomQuerry.first()
		return HttpResponseRedirect('../../' + str(room.pk) + '/')
	# Creating the room if it doesn't exist already
	else:
		room = models.Room.objects.create(
			user1=user1Obj,
			user2=user2Obj,
		)
		return HttpResponseRedirect('../../' + str(room.pk) + '/')


# This function is used to delete a chat_room and it redirects to to the profile page
# (the page from which users would delete a room without entering the url manually)
@login_required
def roomDelete(request, room_pk):
	room = models.Room.objects.get(pk=room_pk)
	if request.user != room.user1.user and request.user != room.user2.user:
		raise PermissionDenied()
	else:
		room.delete()
		return HttpResponseRedirect('/profile/' + str(request.user.pk) + '/')
