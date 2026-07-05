import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, UserStatus, ChatGroup, BroadcastList
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
            
            # Join all ChatGroup channels this user is a member of
            groups = await self.get_user_groups()
            for group_id in groups:
                await self.channel_layer.group_add(f"group_{group_id}", self.channel_name)

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
        print(f"WS RECEIVED DATA: {data}")
        action = data.get('action')
        
        # Handle edits and deletes
        if action == 'edit':
            message_id = data.get('message_id')
            content = data.get('message')
            msg = await self.edit_message(message_id, content)
            if msg:
                event_data = {
                    "type": "message_edit",
                    "message_id": message_id,
                    "message": content
                }
                if msg.group:
                    await self.channel_layer.group_send(f"group_{msg.group.id}", event_data)
                elif msg.receiver:
                    await self.channel_layer.group_send(f"user_{msg.receiver.id}", event_data)
                    await self.channel_layer.group_send(f"user_{msg.sender.id}", event_data)
            return

        if action == 'delete':
            message_id = data.get('message_id')
            # Delete for everyone (only sender can do this)
            msg = await self.delete_message_everyone(message_id)
            if msg:
                event_data = {
                    "type": "message_delete",
                    "message_id": message_id
                }
                if msg.group:
                    await self.channel_layer.group_send(f"group_{msg.group.id}", event_data)
                elif msg.receiver:
                    await self.channel_layer.group_send(f"user_{msg.receiver.id}", event_data)
                    await self.channel_layer.group_send(f"user_{msg.sender.id}", event_data)
            return

        if action == 'broadcast_media':
            message_id = data.get('message_id')
            msg_data = await self.get_serialized_message_by_id(message_id)
            if msg_data:
                event_data = {
                    "type": "chat_message",
                    **msg_data
                }
                if msg_data["is_group"]:
                    await self.channel_layer.group_send(f"group_{msg_data['group_id']}", event_data)
                elif msg_data["is_broadcast"]:
                    members = await self.get_broadcast_members(msg_data["broadcast_id"])
                    for member_id in members:
                        await self.channel_layer.group_send(f"user_{member_id}", event_data)
                    await self.channel_layer.group_send(f"user_{self.user.id}", event_data)
                else:
                    await self.channel_layer.group_send(f"user_{msg_data['receiver_id']}", event_data)
                    await self.channel_layer.group_send(f"user_{self.user.id}", event_data)
            return

        message_content = data.get('message', '')
        receiver_id = data.get('receiver_id')
        is_group = data.get('is_group', False)
        is_broadcast = data.get('is_broadcast', False)
        file_url = data.get('file_url')
        is_image = data.get('is_image', False)
        is_video = data.get('is_video', False)
        is_audio = data.get('is_audio', False)
        temp_id = data.get('temp_id')

        if not message_content and not file_url:
            return

        if is_group:
            # Group Message
            msg = await self.save_group_message(receiver_id, message_content, file_url, is_image, is_video, is_audio)
            if msg:
                await self.channel_layer.group_send(
                    f"group_{receiver_id}",
                    {
                        "type": "chat_message",
                        "message": message_content,
                        "sender_id": str(self.user.id),
                        "sender_username": self.user.username,
                        "file_url": file_url,
                        "is_image": is_image,
                        "is_video": is_video,
                        "is_audio": is_audio,
                        "is_group": True,
                        "group_id": receiver_id,
                        "timestamp": "Just now",
                        "message_id": msg.id,
                        "temp_id": temp_id
                    }
                )
        elif is_broadcast:
            # Broadcast Message: sends individual messages to all list members
            members = await self.get_broadcast_members(receiver_id)
            for member_id in members:
                # Save individual message
                msg = await self.save_direct_message(member_id, message_content, file_url, is_image, is_video, is_audio, broadcast_id=receiver_id)
                if msg:
                    # Send real-time message to receiver
                    await self.channel_layer.group_send(
                        f"user_{member_id}",
                        {
                            "type": "chat_message",
                            "message": message_content,
                            "sender_id": str(self.user.id),
                            "sender_username": self.user.username,
                            "file_url": file_url,
                            "is_image": is_image,
                            "is_video": is_video,
                            "is_audio": is_audio,
                            "is_broadcast": True,
                            "broadcast_id": receiver_id,
                            "timestamp": "Just now",
                            "message_id": msg.id,
                            "temp_id": temp_id
                        }
                    )
            # Send message to sender themselves so their screen updates
            await self.channel_layer.group_send(
                f"user_{self.user.id}",
                {
                    "type": "chat_message",
                    "message": message_content,
                    "sender_id": str(self.user.id),
                    "sender_username": self.user.username,
                    "file_url": file_url,
                    "is_image": is_image,
                    "is_video": is_video,
                    "is_audio": is_audio,
                    "is_broadcast": True,
                    "broadcast_id": receiver_id,
                    "timestamp": "Just now",
                    "temp_id": temp_id
                }
            )
        else:
            # Direct Message
            msg = await self.save_direct_message(receiver_id, message_content, file_url, is_image, is_video, is_audio)
            if msg:
                # Send to receiver
                await self.channel_layer.group_send(
                    f"user_{receiver_id}",
                    {
                        "type": "chat_message",
                        "message": message_content,
                        "sender_id": str(self.user.id),
                        "sender_username": self.user.username,
                        "file_url": file_url,
                        "is_image": is_image,
                        "is_video": is_video,
                        "is_audio": is_audio,
                        "timestamp": "Just now",
                        "message_id": msg.id,
                        "temp_id": temp_id
                    }
                )
                # Send to sender's other sessions
                await self.channel_layer.group_send(
                    f"user_{self.user.id}",
                    {
                        "type": "chat_message",
                        "message": message_content,
                        "sender_id": str(self.user.id),
                        "sender_username": self.user.username,
                        "file_url": file_url,
                        "is_image": is_image,
                        "is_video": is_video,
                        "is_audio": is_audio,
                        "timestamp": "Just now",
                        "message_id": msg.id,
                        "temp_id": temp_id
                    }
                )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "sender_id": str(event["sender_id"]),
            "sender_username": event.get("sender_username", ""),
            "file_url": event.get("file_url"),
            "is_image": event.get("is_image"),
            "is_video": event.get("is_video"),
            "is_audio": event.get("is_audio"),
            "is_group": event.get("is_group", False),
            "group_id": event.get("group_id"),
            "is_broadcast": event.get("is_broadcast", False),
            "broadcast_id": event.get("broadcast_id"),
            "timestamp": event.get("timestamp", "Just now"),
            "message_id": event.get("message_id"),
            "temp_id": event.get("temp_id")
        }))

    async def status_broadcast(self, event):
        await self.send(text_data=json.dumps({
            "type": "status_update",
            "user_id": str(event["user_id"]),
            "status": event["status"]
        }))

    async def message_edit(self, event):
        await self.send(text_data=json.dumps({
            "type": "message_edit",
            "message_id": event["message_id"],
            "message": event["message"]
        }))

    async def message_delete(self, event):
        await self.send(text_data=json.dumps({
            "type": "message_delete",
            "message_id": event["message_id"]
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
    def get_user_groups(self):
        return list(ChatGroup.objects.filter(members=self.user).values_list('id', flat=True))

    @database_sync_to_async
    def get_broadcast_members(self, broadcast_id):
        try:
            b_list = BroadcastList.objects.get(id=broadcast_id, owner=self.user)
            return list(b_list.members.values_list('id', flat=True))
        except BroadcastList.DoesNotExist:
            return []

    @database_sync_to_async
    def save_direct_message(self, receiver_id, content, file_url=None, is_image=False, is_video=False, is_audio=False, broadcast_id=None):
        try:
            receiver = User.objects.get(id=receiver_id)
            msg = Message.objects.create(
                sender=self.user,
                receiver=receiver,
                content=content,
                is_image=is_image
            )
            if broadcast_id:
                msg.broadcast_id = broadcast_id
                
            if file_url:
                # If we passed a media URL from upload
                if is_image: msg.file_upload = file_url
                elif is_video: msg.short_video = file_url
                elif is_audio: msg.voice_note = file_url
                else: msg.document = file_url
                msg.save()
            return msg
        except Exception as e:
            print("Save direct message fail:", e)
            return None

    @database_sync_to_async
    def save_group_message(self, group_id, content, file_url=None, is_image=False, is_video=False, is_audio=False):
        try:
            group = ChatGroup.objects.get(id=group_id, members=self.user)
            msg = Message.objects.create(
                sender=self.user,
                group=group,
                content=content,
                is_image=is_image
            )
            if file_url:
                if is_image: msg.file_upload = file_url
                elif is_video: msg.short_video = file_url
                elif is_audio: msg.voice_note = file_url
                else: msg.document = file_url
                msg.save()
            return msg
        except Exception as e:
            print("Save group message fail:", e)
            return None

    @database_sync_to_async
    def edit_message(self, message_id, content):
        try:
            msg = Message.objects.get(id=message_id, sender=self.user)
            msg.content = content
            msg.is_edited = True
            msg.save()
            return msg
        except Exception:
            return None

    @database_sync_to_async
    def delete_message_everyone(self, message_id):
        try:
            msg = Message.objects.get(id=message_id, sender=self.user)
            msg.is_deleted = True
            msg.content = "This message was deleted"
            # Clear file fields
            if msg.file_upload: msg.file_upload = None
            if msg.voice_note: msg.voice_note = None
            if msg.short_video: msg.short_video = None
            if msg.document: msg.document = None
            msg.save()
            return msg
        except Exception:
            return None

    @database_sync_to_async
    def get_serialized_message_by_id(self, message_id):
        try:
            msg = Message.objects.select_related('sender', 'receiver', 'group', 'broadcast').get(id=message_id)
            file_url = None
            if msg.file_upload:
                file_url = msg.file_upload.url
            elif msg.voice_note:
                file_url = msg.voice_note.url
            elif msg.short_video:
                file_url = msg.short_video.url
            elif msg.document:
                file_url = msg.document.url
                
            return {
                "message": msg.content or "",
                "sender_id": str(msg.sender.id),
                "sender_username": msg.sender.username,
                "file_url": file_url,
                "is_image": msg.is_image,
                "is_video": bool(msg.short_video),
                "is_audio": bool(msg.voice_note),
                "is_group": bool(msg.group),
                "group_id": msg.group.id if msg.group else None,
                "is_broadcast": bool(msg.broadcast),
                "broadcast_id": msg.broadcast.id if msg.broadcast else None,
                "receiver_id": msg.receiver.id if msg.receiver else None,
                "timestamp": msg.timestamp.strftime("%I:%M %p"),
                "message_id": msg.id
            }
        except Message.DoesNotExist:
            return None