from django.shortcuts import render
from . import models
from Users import models as user_models
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

@login_required
def room(request, room_pk=None):
	room = models.Room.objects.get(pk=room_pk)
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


def find_room(request, user_info_pk, current_user_info_pk):

	# the user1 in a chat is the user with the smaller pk
	if user_info_pk < current_user_info_pk:
		user1Obj = user_models.UserInfo.objects.get(pk=user_info_pk)
		user2Obj = user_models.UserInfo.objects.get(pk=current_user_info_pk)
	else:
		user2Obj = user_models.UserInfo.objects.get(pk=user_info_pk)
		user1Obj = user_models.UserInfo.objects.get(pk=current_user_info_pk)

	roomQuerry = models.Room.objects.filter(user1=user1Obj, user2=user2Obj)
	if roomQuerry.exists():
		room = roomQuerry.first()
		return HttpResponseRedirect('../../' + str(room.pk) + '/')
	else: 
		room = models.Room.objects.create(
			user1 = user1Obj,
			user2 = user2Obj,
		)
		return HttpResponseRedirect('../../' + str(room.pk) + '/')

def roomDelete(request, room_pk):
    room = models.Room.objects.get(pk=room_pk)
    room.delete()
    return HttpResponseRedirect('/profile/' + str(request.user.pk) + '/')

