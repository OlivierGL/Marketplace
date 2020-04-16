from channels.generic.websocket import WebsocketConsumer
import json
import asyncio
from asgiref.sync import async_to_sync
from Users import models as users_models
from . import models
from django.utils.timezone import localtime

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.room_name = str(self.scope['url_route']['kwargs']['room_pk'])
		self.room_group_name = 'chat_%s' % self.room_name
		# Join room
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		user = self.scope['user']
		if user.is_authenticated:
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

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		user = self.scope['user']
		if user.is_authenticated:
			#create new message object in database	
			room_pk = self.room_name
			roomObj = models.Room.objects.get(pk=room_pk)
			messageObj = models.Message.objects.create(
				room=roomObj,
				sender=users_models.UserInfo.objects.get(user=user),
				content=message,
				)
			message = '('+ localtime(messageObj.time_sent).strftime('%Y-%m-%d %H:%M') + ') '+ user.first_name + ' sent: ' + message
		else:
			message = 'Anonymous: ' + message

		# Send message to room group
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message
			}
		)


	def chat_message(self, event):
		message = event['message']
		self.send(text_data=json.dumps({
			'message': message
		}))

	def logout(self):
		pass