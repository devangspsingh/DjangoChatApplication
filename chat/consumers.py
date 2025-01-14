from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import ChatMessage
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = f"chat_{min(self.user.id, self.other_user_id)}_{max(self.user.id, self.other_user_id)}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        sender = self.user
        receiver = await sync_to_async(User.objects.get)(id=self.other_user_id)  # Wrap ORM call

        # Save the message to the database
        chat_message = await sync_to_async(ChatMessage.objects.create)(
            sender=sender, receiver=receiver, message=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'seen': chat_message.seen,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
