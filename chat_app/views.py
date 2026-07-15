from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Max, OuterRef, Subquery, DateTimeField
from django.contrib.auth import get_user_model
from .models import Message, ChatGroup, BroadcastList, MessageReaction, Poll, PollOption, PollVote
from .serializers import MessageSerializer, ChatGroupSerializer, BroadcastListSerializer

User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        })

# ────────────────────────────────────────────────────────
# 👥 பயனர் பட்டியல் (Return ALL users for the user selector modal)
# ────────────────────────────────────────────────────────
class ChatUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        all_users = User.objects.exclude(id=current_user.id).order_by('username')
        
        user_list = []
        for user in all_users:
            is_online = False
            if hasattr(user, 'userstatus'):
                is_online = user.userstatus.is_online

            user_list.append({
                "id": user.id,
                "username": user.username,
                "is_online": is_online,
                "unread_count": 0,
                "last_message": "Start a new conversation",
                "last_msg_time": ""
            })
        
        return Response(user_list)


# ────────────────────────────────────────────────────────
# 💬 Unified Active Conversations List (History only)
# ────────────────────────────────────────────────────────
class ConversationsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        current_user = request.user
        conversations = []
        
        # Helper to get last message details
        def get_msg_details(msg, current_user):
            if not msg:
                return "No messages yet", "", 0, None
            unread_cnt = 0
            if msg.sender != current_user and not msg.is_read:
                unread_cnt = 1
            preview = msg.content or ""
            if not preview:
                if msg.file_upload: preview = "📷 Image" if msg.is_image else "📄 Document"
                elif msg.voice_note: preview = "🎙️ Voice note"
                elif msg.short_video: preview = "🎥 Short Video"
                else: preview = "Attachment"
            return preview, msg.timestamp.strftime('%I:%M %p') if msg.timestamp else "", unread_cnt, msg.timestamp
            
        # 1. Direct Chats with history
        direct_users = User.objects.filter(
            Q(chat_received_messages__sender=current_user) | 
            Q(chat_sent_messages__receiver=current_user)
        ).distinct().exclude(id=current_user.id)
        
        for u in direct_users:
            last_msg = Message.objects.filter(
                (Q(sender=current_user) & Q(receiver=u)) |
                (Q(sender=u) & Q(receiver=current_user))
            ).exclude(deleted_by=current_user).order_by('-timestamp').first()
            
            if last_msg:
                last_text, last_time, unread_count, raw_time = get_msg_details(last_msg, current_user)
                unread_count = Message.objects.filter(sender=u, receiver=current_user, is_read=False).exclude(deleted_by=current_user).count()
                
                conversations.append({
                    "id": u.id,
                    "username": u.username,
                    "is_group": False,
                    "is_broadcast": False,
                    "is_online": u.userstatus.is_online if hasattr(u, 'userstatus') else False,
                    "unread_count": unread_count,
                    "last_message": last_text,
                    "last_msg_time": last_time,
                    "last_msg_timestamp": raw_time.isoformat() if raw_time else ""
                })
                
        # 2. Groups current user is in
        groups = ChatGroup.objects.filter(members=current_user)
        for g in groups:
            last_msg = Message.objects.filter(group=g).exclude(deleted_by=current_user).order_by('-timestamp').first()
            last_text, last_time, unread_count, raw_time = get_msg_details(last_msg, current_user)
            if not raw_time:
                raw_time = g.created_at
                last_time = g.created_at.strftime('%I:%M %p')
                
            conversations.append({
                "id": g.id,
                "username": g.name,
                "is_group": True,
                "is_broadcast": False,
                "is_online": False,
                "unread_count": 0,
                "last_message": last_text,
                "last_msg_time": last_time,
                "last_msg_timestamp": raw_time.isoformat() if raw_time else ""
            })
            
        # 3. Broadcast lists current user owns
        broadcasts = BroadcastList.objects.filter(owner=current_user)
        for b in broadcasts:
            last_msg = Message.objects.filter(broadcast=b).exclude(deleted_by=current_user).order_by('-timestamp').first()
            last_text, last_time, unread_count, raw_time = get_msg_details(last_msg, current_user)
            if not raw_time:
                raw_time = b.created_at
                last_time = b.created_at.strftime('%I:%M %p')
                
            conversations.append({
                "id": b.id,
                "username": b.name,
                "is_group": False,
                "is_broadcast": True,
                "is_online": False,
                "unread_count": 0,
                "last_message": last_text,
                "last_msg_time": last_time,
                "last_msg_timestamp": raw_time.isoformat() if raw_time else ""
            })
            
        conversations.sort(key=lambda x: x["last_msg_timestamp"] or "", reverse=True)
        return Response(conversations)


# ────────────────────────────────────────────────────────
# 👥 CRUD Groups
# ────────────────────────────────────────────────────────
class GroupListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        groups = ChatGroup.objects.filter(members=request.user)
        serializer = ChatGroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description', '')
        member_ids = request.data.get('members', [])
        
        if not name:
            return Response({"error": "Group name is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        group = ChatGroup.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        group.admins.add(request.user)
        group.members.add(request.user)
        
        for m_id in member_ids:
            try:
                group.members.add(User.objects.get(id=m_id))
            except User.DoesNotExist:
                pass
                
        serializer = ChatGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GroupDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            group = ChatGroup.objects.get(pk=pk, members=request.user)
        except ChatGroup.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatGroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            group = ChatGroup.objects.get(pk=pk, admins=request.user)
        except ChatGroup.DoesNotExist:
            return Response({"error": "Group not found or not admin"}, status=status.HTTP_404_NOT_FOUND)
            
        name = request.data.get('name')
        description = request.data.get('description')
        member_ids = request.data.get('members')
        
        if name:
            group.name = name
        if description is not None:
            group.description = description
        group.save()
        
        if member_ids is not None:
            group.members.clear()
            group.members.add(request.user)
            for m_id in member_ids:
                try:
                    group.members.add(User.objects.get(id=m_id))
                except User.DoesNotExist:
                    pass
                    
        serializer = ChatGroupSerializer(group)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            group = ChatGroup.objects.get(pk=pk, admins=request.user)
        except ChatGroup.DoesNotExist:
            return Response({"error": "Group not found or not admin"}, status=status.HTTP_404_NOT_FOUND)
        group.delete()
        return Response({"status": "Group deleted"}, status=status.HTTP_204_NO_CONTENT)


# ────────────────────────────────────────────────────────
# 📢 CRUD Broadcasts
# ────────────────────────────────────────────────────────
class BroadcastListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        broadcasts = BroadcastList.objects.filter(owner=request.user)
        serializer = BroadcastListSerializer(broadcasts, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        member_ids = request.data.get('members', [])
        
        if not name:
            return Response({"error": "Broadcast name is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        broadcast = BroadcastList.objects.create(
            name=name,
            owner=request.user
        )
        for m_id in member_ids:
            try:
                broadcast.members.add(User.objects.get(id=m_id))
            except User.DoesNotExist:
                pass
                
        serializer = BroadcastListSerializer(broadcast)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BroadcastDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            broadcast = BroadcastList.objects.get(pk=pk, owner=request.user)
        except BroadcastList.DoesNotExist:
            return Response({"error": "Broadcast list not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BroadcastListSerializer(broadcast)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            broadcast = BroadcastList.objects.get(pk=pk, owner=request.user)
        except BroadcastList.DoesNotExist:
            return Response({"error": "Broadcast list not found"}, status=status.HTTP_404_NOT_FOUND)
            
        name = request.data.get('name')
        member_ids = request.data.get('members')
        
        if name:
            broadcast.name = name
            broadcast.save()
            
        if member_ids is not None:
            broadcast.members.clear()
            for m_id in member_ids:
                try:
                    broadcast.members.add(User.objects.get(id=m_id))
                except User.DoesNotExist:
                    pass
                    
        serializer = BroadcastListSerializer(broadcast)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            broadcast = BroadcastList.objects.get(pk=pk, owner=request.user)
        except BroadcastList.DoesNotExist:
            return Response({"error": "Broadcast list not found"}, status=status.HTTP_404_NOT_FOUND)
        broadcast.delete()
        return Response({"status": "Broadcast list deleted"}, status=status.HTTP_204_NO_CONTENT)


# ────────────────────────────────────────────────────────
# 📜 சாட் ஹிஸ்டரி (Chat History API with Filters)
# ────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request, user_id):
    logged_in_user = request.user
    chat_type = request.GET.get('type', 'user') # 'user', 'group', 'broadcast'
    
    if chat_type == 'group':
        messages = Message.objects.filter(group_id=user_id)
    elif chat_type == 'broadcast':
        messages = Message.objects.filter(broadcast_id=user_id)
    else:
        messages = Message.objects.filter(
            (Q(sender=logged_in_user) & Q(receiver_id=user_id)) |
            (Q(sender_id=user_id) & Q(receiver=logged_in_user))
        )
    
    # Exclude messages deleted by current user (Delete for me)
    messages = messages.exclude(deleted_by=logged_in_user).order_by('timestamp')
    
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)


# ────────────────────────────────────────────────────────
# 📎 ஃபைல் அப்லோடு (File Upload API for Group/Broadcast/User)
# ────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file_api(request):
    sender = request.user
    receiver_id = request.data.get('receiver_id')
    group_id = request.data.get('group_id')
    broadcast_id = request.data.get('broadcast_id')
    
    file = request.FILES.get('file')
    is_image = request.data.get('is_image', 'false') == 'true'
    is_audio = request.data.get('is_audio', 'false') == 'true'
    is_video = request.data.get('is_video', 'false') == 'true'
    content = request.data.get('content', '')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    msg_kwargs = {
        'sender': sender,
        'content': content,
    }
    
    if is_image:
        msg_kwargs['file_upload'] = file
        msg_kwargs['is_image'] = True
    elif is_audio:
        msg_kwargs['voice_note'] = file
    elif is_video:
        msg_kwargs['short_video'] = file
    else:
        msg_kwargs['document'] = file

    if group_id:
        msg_kwargs['group'] = ChatGroup.objects.get(id=group_id)
    elif broadcast_id:
        msg_kwargs['broadcast'] = BroadcastList.objects.get(id=broadcast_id)
    elif receiver_id:
        msg_kwargs['receiver'] = User.objects.get(id=receiver_id)
    else:
        return Response({"error": "Recipient not specified"}, status=400)

    msg = Message.objects.create(**msg_kwargs)
    serializer = MessageSerializer(msg)
    return Response(serializer.data)


# ────────────────────────────────────────────────────────
# 🗑️ மெசேஜ்களை நீக்குதல் (Delete for Everyone / Delete for Me)
# ────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_message_api(request, message_id):
    current_user = request.user
    delete_type = request.data.get('delete_type', 'me') # 'everyone' or 'me'
    
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=404)
        
    if delete_type == 'everyone':
        if message.sender != current_user:
            return Response({"error": "Only sender can delete for everyone"}, status=403)
        message.is_deleted = True
        message.content = "This message was deleted"
        if message.file_upload:
            message.file_upload.delete(save=False)
            message.file_upload = None
        if message.voice_note:
            message.voice_note.delete(save=False)
            message.voice_note = None
        if message.short_video:
            message.short_video.delete(save=False)
            message.short_video = None
        if message.document:
            message.document.delete(save=False)
            message.document = None
        message.save()
        
        # Broadcast deletion over WebSocket
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        if message.group:
            async_to_sync(channel_layer.group_send)(
                f"group_{message.group.id}",
                {"type": "message_delete", "message_id": message.id}
            )
        elif message.broadcast:
            for member in message.broadcast.members.all():
                async_to_sync(channel_layer.group_send)(
                    f"user_{member.id}",
                    {"type": "message_delete", "message_id": message.id}
                )
            async_to_sync(channel_layer.group_send)(
                f"user_{message.sender.id}",
                {"type": "message_delete", "message_id": message.id}
            )
        elif message.receiver:
            async_to_sync(channel_layer.group_send)(
                f"user_{message.receiver.id}",
                {"type": "message_delete", "message_id": message.id}
            )
            async_to_sync(channel_layer.group_send)(
                f"user_{message.sender.id}",
                {"type": "message_delete", "message_id": message.id}
            )
        return Response({"status": "Deleted for everyone"})
    else:
        message.deleted_by.add(current_user)
        return Response({"status": "Deleted for me"})


# ────────────────────────────────────────────────────────
# 👁️ மெசேஜ்களைப் படித்ததாக மாற்றுதல் (Mark Read API)
# ────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_messages_as_read(request, user_id):
    current_user = request.user
    Message.objects.filter(
        sender_id=user_id,
        receiver=current_user,
        is_read=False
    ).update(is_read=True)
    return Response({"status": "Messages marked as read"}, status=200)