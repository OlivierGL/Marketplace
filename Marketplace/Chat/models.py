from django.db import models

from Users.models import UserInfo


# Chat object that stores the two users in a chat
class Room(models.Model):
    user1 = models.ForeignKey(UserInfo, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserInfo, related_name='user2', on_delete=models.CASCADE)


# Message object that store the room in which a message belongs, the sender, the content
# and the time at which it was sent. This model is used to keep messages in memory 
# and print them in the chats so that users don't miss messages and they can go 
# back to look up previous messages.
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserInfo, related_name='sender', on_delete=models.CASCADE)
    content = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)
