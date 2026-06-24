import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, UserStatus
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken 

User = get_user_model()

class WhatsAppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user and self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            
            subprotocols = self.scope.get('subprotocols', [])
            if subprotocols:
                await self.accept(subprotocols[0]) 
            else:
                await self.accept()
            
            await self.update_user_status(True)
            await self.channel_layer.group_add("global_status", self.channel_name)
            await self.channel_layer.group_send("global_status", {"type": "status_broadcast", "user_id": self.user.id, "status": True})
        else:
            print("WebSocket Reject: User is Anonymous. Connection closed.")
            await self.close()

    async def disconnect(self, close_code):
        if self.user and self.user.is_authenticated:
            await self.update_user_status(False)
            await self.channel_layer.group_send("global_status", {"type": "status_broadcast", "user_id": self.user.id, "status": False})
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message')
        receiver_id = data.get('receiver_id')

        if not message_content or not receiver_id:
            return

        # DB-il message text save seiyal
        msg = await self.save_text_message(receiver_id, message_content)

        # 🚀 Receiver group-க்கு மெசேஜ் அனுப்பும்போது `str(self.user.id)` என ஸ்ட்ரிங் ஆக மாற்றி அனுப்புகிறோம்!
        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            {
                "type": "chat_message",
                "message": message_content,
                "sender_id": str(self.user.id),  # 👈 ஜாவாஸ்கிரிப்ட் டைப் இடிக்காமல் இருக்க 'str' ஆக மாற்றப்பட்டுள்ளது
                "file_url": None,
                "is_image": False,
                "timestamp": "Just now"
            }
        )

    # 🟢 ரியல் வாட்ஸ்அப் நோட்டிபிகேஷன் மேஜிக் நடக்கும் இடம்
    async def chat_message(self, event):
        # ரியாக்ட் எதிர்பார்க்கும் அதே வடிவில் துல்லியமாக டேட்டாவை பில்டர் செய்து அனுப்புகிறோம்
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "sender_id": str(event["sender_id"]), # 👈 ஸ்ட்ரிங் ஐடி
            "file_url": event.get("file_url"),
            "is_image": event.get("is_image"),
            "timestamp": event.get("timestamp", "Just now")
        }))

    async def status_broadcast(self, event):
        await self.send(text_data=json.dumps({
            "type": "status_update",
            "user_id": str(event["user_id"]), # 👈 இங்கேயும் ஸ்ட்ரிங் ஆக்கியாச்சு
            "status": event["status"]
        }))

    @database_sync_to_async
    def get_user_from_jwt(self, token_string):
        try:
            validated_token = AccessToken(token_string)
            user_id = validated_token['user_id']
            return User.objects.get(id=user_id)
        except Exception as e:
            print("JWT Socket Auth Error:", e)
            return None

    @database_sync_to_async
    def update_user_status(self, status):
        user_status, created = UserStatus.objects.get_or_create(user=self.user)
        user_status.is_online = status
        user_status.save()

    @database_sync_to_async
    def save_text_message(self, receiver_id, content):
        receiver = User.objects.get(id=receiver_id)
        return Message.objects.create(sender=self.user, receiver=receiver, content=content)