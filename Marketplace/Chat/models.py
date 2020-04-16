from django.db import models
from Users.models import UserInfo

# Create your models here.

# Chat table that only stores the two users in a chat
class Room(models.Model):
    user1 = models.ForeignKey(UserInfo, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserInfo, related_name='user2', on_delete=models.CASCADE)

class Message(models.Model):
	room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
	sender = models.ForeignKey(UserInfo, related_name='sender', on_delete=models.CASCADE)
	content = models.TextField()
	time_sent = models.DateTimeField(auto_now_add=True)



