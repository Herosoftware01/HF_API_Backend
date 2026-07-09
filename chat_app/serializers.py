from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, UserStatus

User = get_user_model()

class UserChatStatusSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField(source='status.is_online', read_only=True)
    last_seen = serializers.DateTimeField(source='status.last_seen', read_only=True)
    hide_last_seen = serializers.BooleanField(source='status.hide_last_seen', read_only=True)
    hide_profile_photo = serializers.BooleanField(source='status.hide_profile_photo', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_online', 'last_seen', 'hide_last_seen', 'hide_profile_photo']


from .models import ChatGroup, BroadcastList, MessageReaction, Poll, PollOption

class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'


class BroadcastListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroadcastList
        fields = '__all__'


class MessageReactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = MessageReaction
        fields = ['id', 'user', 'username', 'emoji', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    timestamp_formatted = serializers.SerializerMethodField()
    reactions = MessageReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_username', 'receiver', 'group', 'broadcast', 
            'content', 'reply_to', 'is_forwarded', 'is_edited', 'is_deleted',
            'file_upload', 'is_image', 'voice_note', 'short_video', 'document',
            'location_lat', 'location_long', 'contact_data',
            'timestamp', 'timestamp_formatted', 'is_read', 'reactions'
        ]

    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime("%I:%M %p") # 04:30 PM WhatsApp Style