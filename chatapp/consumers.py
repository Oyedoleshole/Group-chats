import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chatapp.models import *
from django.contrib.auth import get_user_model
from .serializers import CustomSerializer

class Privatechat(AsyncWebsocketConsumer):
    async def connect(self):
        print("Initial connection is working")
        self.user = self.scope['url_route']['kwargs']['user']
        self.joinee_user = self.scope['url_route']['kwargs']['joinee_user']
        self.room_name = f"{self.user}_{self.joinee_user}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        print("Initial connection is end")
    
    async def disconnect(self, code):
        print("Disconnecting socket is working")
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        # await self.disconnect(code)
        print("Disconnecting socket is end")

    async def receive(self, text_data=None):
        print("Receiver is working")
        data = json.loads(text_data)
        print(data)
        target_channel_name = f"{data['receiver']}_{data['sender']}"
        event = {
            'type': 'private_chat',
            'user': data['sender'],
            'receiver': data['receiver'],
            'message': data['message'],
            'time': data['time']
        }
        await self.channel_layer.group_send(target_channel_name, event)
        print("Receiver is end")


    async def private_chat(self, event):
        data = event
        print("The data is ====>",data)
        response_data = {
            'user': data['user'],
            'receiver':data['receiver'],
            'message': data['message'],
            'time':data['time']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        self.user_id = self.scope['url_route']['kwargs']['user']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json
        user = text_data_json['sender']
        event = {
            'type': 'send_message',
            'message': message,
            'senderUsername':user,
        }
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message'],
            'time': data['time']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        if not Message.objects.filter(message=data['message']).exists():
            new_message = Message(room=get_room_by_name, sender=data['sender'], message=data['message'])
            new_message.save()