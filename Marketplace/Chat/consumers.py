from channels.generic.websocket import WebsocketConsumer
import json
import asyncio
from asgiref.sync import async_to_sync
from Users import models as users_models
from . import models
from django.utils.timezone import localtime

#Chat consumer that handles the websocket connections. 
class ChatConsumer(WebsocketConsumer):
	
  #Method that handles the initial connection.
  def connect(self):
    self.room_name = str(self.scope['url_route']['kwargs']['room_pk'])
    self.room_group_name = 'chat_%s' % self.room_name
    # Join room
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name
    )
    user = self.scope['user']
    async_to_sync(self.channel_layer.group_add)(
      user.username,
      self.channel_name
    )
    self.accept()

  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name,
      self.channel_name
    )

  # Method that handles received data
  def receive(self, text_data):
    # Getting the message string.
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    user = self.scope['user']

    #create new message object in database	
    room_pk = self.room_name
    roomObj = models.Room.objects.get(pk=room_pk)

    messageObj = models.Message.objects.create(
      room=roomObj,
      sender=users_models.UserInfo.objects.get(user=user),
      content=message,
    )

    # Formatting the message with the time at which it was sent and the user's first name
    message = '('+ localtime(messageObj.time_sent).strftime('%Y-%m-%d %H:%M') + ') '+ user.first_name + ' sent: ' + message

    # Send message to chat room 
    async_to_sync(self.channel_layer.group_send)(
    self.room_group_name,
    {
      'type': 'chat_message',
      'message': message
    })

  # Method that handles received data that is classified as a chat_message. 
  # Sends the message content.
  def chat_message(self, event):
    message = event['message']
    self.send(text_data=json.dumps({
      'message': message
    }))

