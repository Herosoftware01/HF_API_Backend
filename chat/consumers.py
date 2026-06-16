import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message, Profile
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope['url_route']['kwargs']['room_id']

        self.room_group_name = f'chat_{self.room_id}'

        self.user = self.scope['user']

        print("ROOM ID:", self.room_id)
        print("USER:", self.user)

        if not self.user.is_authenticated:
            print("NOT LOGGED IN")
            await self.close()
            return

        is_member = await self.check_room_member()

        print("IS MEMBER:", is_member)

        if not is_member:
            print("USER NOT MEMBER")
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        print("WEBSOCKET CONNECTED")


    async def disconnect(self, close_code):

        if hasattr(self, 'room_group_name'):

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        if hasattr(self, 'user') and self.user.is_authenticated:

            await self.set_online(False)

        print("WEBSOCKET DISCONNECTED")


    async def receive(self, text_data):

        data = json.loads(text_data)

        msg_type = data.get('type', 'chat_message')

        if msg_type == 'chat_message':

            content = data.get('message', '')

            message = await self.save_message(content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': message.id,
                    'message': content,
                    'sender_id': self.user.id,
                    'sender_name': self.user.username,
                    'avatar': await self.get_avatar(),
                    'timestamp': message.timestamp.strftime('%I:%M %p'),
                    'file': None,
                    'file_name': '',
                    'file_type': '',
                }
            )

        elif msg_type == 'typing':

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'sender_id': self.user.id,
                    'sender_name': self.user.username,
                    'is_typing': data.get('is_typing', False)
                }
            )


    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'avatar': event['avatar'],
            'timestamp': event['timestamp'],
            'file': event.get('file'),
            'file_name': event.get('file_name', ''),
            'file_type': event.get('file_type', ''),
        }))


    async def typing_indicator(self, event):

        if event['sender_id'] != self.user.id:

            await self.send(text_data=json.dumps({
                'type': 'typing',
                'sender_name': event['sender_name'],
                'is_typing': event['is_typing']
            }))


    async def user_status(self, event):

        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'is_online': event['is_online']
        }))


    @database_sync_to_async
    def save_message(self, content):

        room = Room.objects.get(id=self.room_id)

        return Message.objects.create(
            room=room,
            sender=self.user,
            content=content
        )


    @database_sync_to_async
    def set_online(self, status):

        Profile.objects.filter(user=self.user).update(
            is_online=status,
            last_seen=timezone.now()
        )


    @database_sync_to_async
    def get_avatar(self):

        try:

            p = self.user.profile

            return p.avatar.url if p.avatar else None

        except:

            return None


    @database_sync_to_async
    def check_room_member(self):

        try:

            print("CHECKING ROOM:", self.room_id, self.user)

            room = Room.objects.get(id=self.room_id)
            exists = room.members.filter(id=self.user.id).exists()

            print("MEMBER EXISTS:", exists)

            return exists

        except Exception as e:

            print("ROOM ERROR:", e)

            return False